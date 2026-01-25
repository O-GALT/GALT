#!/bin/sh
set -e

celery -A GALT beat -l info