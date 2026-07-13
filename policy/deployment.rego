package main

import rego.v1

# Sensitive/well-known infrastructure ports that shouldn't be exposed by a
# regular application container (ssh, db, admin, remote-access ports, etc).
sensitive_ports := {22, 23, 25, 111, 135, 139, 445, 1433, 1521, 2049, 2375,
                     2376, 3306, 3389, 5432, 5900, 5984, 6379, 9200, 9300,
                     11211, 27017}

is_deployment if {
  input.kind == "Deployment"
}

# --- Containers must not run as root ---

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  not container.securityContext.runAsNonRoot == true
  msg := sprintf("container '%s' debe definir securityContext.runAsNonRoot=true (no debe correr como root)", [container.name])
}

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  container.securityContext.runAsUser == 0
  msg := sprintf("container '%s' no debe definir runAsUser=0 (root)", [container.name])
}

# --- No privilege escalation / privileged containers ---

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  container.securityContext.privileged == true
  msg := sprintf("container '%s' no debe correr en modo privileged", [container.name])
}

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  not container.securityContext.allowPrivilegeEscalation == false
  msg := sprintf("container '%s' debe definir securityContext.allowPrivilegeEscalation=false", [container.name])
}

# --- Drop all Linux capabilities by default ---

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  caps := container.securityContext.capabilities.drop
  not "ALL" in caps
  msg := sprintf("container '%s' debe hacer drop de la capability 'ALL'", [container.name])
}

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  not container.securityContext.capabilities.drop
  msg := sprintf("container '%s' no define securityContext.capabilities.drop", [container.name])
}

# --- No host networking / host ports ---

deny contains msg if {
  is_deployment
  input.spec.template.spec.hostNetwork == true
  msg := "el pod no debe usar hostNetwork (expone todos los puertos del nodo host)"
}

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  port := container.ports[_]
  port.hostPort
  msg := sprintf("container '%s' no debe exponer hostPort (%d), evita bindear directamente al puerto del nodo", [container.name, port.hostPort])
}

# --- No sensitive/well-known infra ports exposed ---

deny contains msg if {
  is_deployment
  container := input.spec.template.spec.containers[_]
  port := container.ports[_]
  port.containerPort in sensitive_ports
  msg := sprintf("container '%s' expone el puerto sensible %d (ssh/db/admin), revisa si realmente debe estar expuesto", [container.name, port.containerPort])
}
