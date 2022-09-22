/*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

const pkg_pk = "045795ba59f3e6306779f714248c4051dd1b977808a87b0bd4b2de81a19114520"; // 65 bytes
const car_pk = "045795ba59f3e6306779f714248c4051dd1b977808a87b0bd4b2de81a19114520"; // 65 bytes
const W = "045795ba59f3e6306779f714248c4051dd1b977808a87b0bd4b2de81a19114520"; // 65 bytes
const H = "045795ba59f3e6306779f714248c4051"; // 32 bytes
const sta = 1;

/**
 * Workload module for the benchmark round.
 */
class initVIDWorkload extends WorkloadModuleBase {
    /**
     * Initializes the workload module instance.
     */
    constructor() {
        super();
        this.txIndex = 0;
    }

    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
    async submitTransaction() {
        this.txIndex++;
        let car_id = 'Client' + this.workerIndex + '_VID' + this.txIndex.toString();

        let args = {
            contractId: 'fabcar',
            contractVersion: 'v1',
            contractFunction: 'initVID',
            contractArguments: [car_id, H, pkg_pk, car_pk, W, sta],
            timeout: 30
        };

        await this.sutAdapter.sendRequests(args);
    }
}

/**
 * Create a new instance of the workload module.
 * @return {WorkloadModuleInterface}
 */
function createWorkloadModule() {
    return new initVIDWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
