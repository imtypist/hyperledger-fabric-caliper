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

const { Contract } = require('fabric-contract-api');

class FabCar extends Contract {

    async init(){
        return;
    }

    async initPKG(ctx, pkg_id, pkg_pk) {
        console.info('============= START : init PKG ===========');

        await ctx.stub.putState(pkg_id, Buffer.from(pkg_pk));
        console.info('============= END : init PKG ===========');
    }

    async initVID(ctx, car_id, H, pkg_pk, car_pk, W, sta) {
        console.info('============= START : init VID ===========');

        const car = {
            H,
            pkg_pk,
            car_pk,
            W,
            sta,
        };

        await ctx.stub.putState(car_id, Buffer.from(JSON.stringify(car)));
        console.info('============= END : init VID ===========');
    }

    async queryPKG(ctx, pkg_id) {
        const pkgAsBytes = await ctx.stub.getState(pkg_id); // get the pkg_pk from chaincode state
        if (!pkgAsBytes || pkgAsBytes.length === 0) {
            throw new Error(`${pkg_id} does not exist`);
        }
        console.log(pkgAsBytes.toString());
        return pkgAsBytes.toString();
    }

    async queryVID(ctx, car_id) {
        const carAsBytes = await ctx.stub.getState(car_id); // get the car from chaincode state
        if (!carAsBytes || carAsBytes.length === 0) {
            throw new Error(`${car_id} does not exist`);
        }
        console.log(carAsBytes.toString());
        return carAsBytes.toString();
    }

}

module.exports = FabCar;
