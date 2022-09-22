#!/bin/bash
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Print all commands.
set -v

# Grab the parent directory.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}"

npm i

# bind during CI tests, using the package dir as CWD
# Note: do not use env variables for binding settings, as subsequent launch calls will pick them up and bind again
if [[ "${BIND_IN_PACKAGE_DIR}" = "true" ]]; then
    pushd $SUT_DIR
    ${CALL_METHOD} bind --caliper-bind-sut besu:latest
    popd
fi

# change default settings (add config paths too)
export CALIPER_PROJECTCONFIG=../caliper.yaml

dispose () {
    # dump some container information in case of an error before tearing down the network
    echo "########### Container states and logs"
    docker ps -a
    docker logs --tail 50 besu_clique
    echo ""
    ${CALL_METHOD} launch manager --caliper-workspace phase1 --caliper-flow-only-end
}

# PHASE 1: just starting the network
${CALL_METHOD} launch manager --caliper-workspace phase1 --caliper-flow-only-start
rc=$?
if [[ ${rc} != 0 ]]; then
    echo "Failed CI step 1";
    dispose;
    exit ${rc};
fi

# PHASE 2: single caliper client, estimate gas on open
${CALL_METHOD} launch manager --caliper-workspace phase2 --caliper-flow-skip-start --caliper-flow-skip-end
rc=$?
if [[ ${rc} != 0 ]]; then
    echo "Failed CI step 2";
    dispose;
    exit ${rc};
fi

# PHASE 3: multiple caliper clients, all gas fixed
${CALL_METHOD} launch manager --caliper-workspace phase3 --caliper-flow-skip-start --caliper-flow-skip-end
rc=$?
if [[ ${rc} != 0 ]]; then
    echo "Failed CI step 3";
    dispose;
    exit ${rc};
fi

# PHASE 4: private transactions
${CALL_METHOD} launch manager --caliper-workspace privatetxs --caliper-flow-skip-start --caliper-flow-skip-end
rc=$?
if [[ ${rc} != 0 ]]; then
    echo "Failed CI step 4 - private txs";
    dispose;
    exit ${rc};
fi

# PHASE 5: just disposing of the network
${CALL_METHOD} launch manager --caliper-workspace phase1 --caliper-flow-only-end
rc=$?
if [[ ${rc} != 0 ]]; then
    echo "Failed CI step 5";
    exit ${rc};
fi
