#!/bin/bash

cdk bootstrap aws://$ACCOUNT_NUMBER/$REGION
cdk synth
