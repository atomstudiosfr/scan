#!/bin/sh

## Promtail
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --values promtail-values.yaml --install promtail grafana/promtail

# PostgreSQL

