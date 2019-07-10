#!/bin/bash
dockerc=docker-compose
$dockerc -f docker-compose-test.yml down &&
    $dockerc -f docker-compose-test.yml up -d mongo api-falcon listener ganachecli &&
    $dockerc -f docker-compose-test.yml up test-truffle
