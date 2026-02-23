#!/bin/sh

#O shell irá encerrar a execução do script se algum comando retornar um código de erro diferente de zero
set -e

wait_psql.sh
collectstatic.sh
makemigrations.sh
migrate.sh
runserver.sh