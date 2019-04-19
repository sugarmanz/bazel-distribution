#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys
import re


def parse_deployment_properties(fn):
    deployment_properties = {}
    with open(fn) as deployment_properties_file:
        for line in deployment_properties_file.readlines():
            if line.startswith('#'):
                # skip comments
                pass
            elif '=' in line:
                k, v = line.split('=')
                deployment_properties[k] = v.strip()
    return deployment_properties


_, rules_template_fn, rules_output, deployment_properties_fn, deployment_properties_lbl = sys.argv


with open(rules_template_fn) as rules_template_file:
    rules_template = "# DO NOT EDIT THIS FILE!\n" \
                     "# Autogenerated by @graknlabs_bazel_distribution//maven:deployment_rules_builder.py\n\n\n"
    rules_template += rules_template_file.read()

properties = parse_deployment_properties(deployment_properties_fn)

SUBSTITUTIONS = {
    '{deployment_properties_placeholder}': deployment_properties_lbl,
    '{maven_packages}': properties['maven.packages']
}

for original, substitution in SUBSTITUTIONS.items():
    rules_template = re.sub(original, substitution, rules_template)

with open(rules_output, 'w') as rules_bzl:
    rules_bzl.write(rules_template)
