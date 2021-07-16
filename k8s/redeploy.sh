#!/bin/bash

set -x
NS=iaas-awesom-o

kubectl delete -f wibot.yml
kubectl delete configmap wibot-users --namespace=$NS

kubectl create configmap wibot-users --from-file=users.properties=./users.properties --namespace=$NS
kubectl create -f wibot.yml
