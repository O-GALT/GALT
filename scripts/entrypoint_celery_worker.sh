#!/bin/sh
set -e

celery -A GALT worker -l info