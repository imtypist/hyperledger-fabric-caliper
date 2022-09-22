// Code generated by counterfeiter. DO NOT EDIT.
package mock

import (
	"sync"

	"github.com/hyperledger/fabric/core/chaincode/lifecycle"
	"github.com/hyperledger/fabric/core/ledger"
)

type QueryExecutorProvider struct {
	TxQueryExecutorStub        func(string, string) ledger.SimpleQueryExecutor
	txQueryExecutorMutex       sync.RWMutex
	txQueryExecutorArgsForCall []struct {
		arg1 string
		arg2 string
	}
	txQueryExecutorReturns struct {
		result1 ledger.SimpleQueryExecutor
	}
	txQueryExecutorReturnsOnCall map[int]struct {
		result1 ledger.SimpleQueryExecutor
	}
	invocations      map[string][][]interface{}
	invocationsMutex sync.RWMutex
}

func (fake *QueryExecutorProvider) TxQueryExecutor(arg1 string, arg2 string) ledger.SimpleQueryExecutor {
	fake.txQueryExecutorMutex.Lock()
	ret, specificReturn := fake.txQueryExecutorReturnsOnCall[len(fake.txQueryExecutorArgsForCall)]
	fake.txQueryExecutorArgsForCall = append(fake.txQueryExecutorArgsForCall, struct {
		arg1 string
		arg2 string
	}{arg1, arg2})
	fake.recordInvocation("TxQueryExecutor", []interface{}{arg1, arg2})
	fake.txQueryExecutorMutex.Unlock()
	if fake.TxQueryExecutorStub != nil {
		return fake.TxQueryExecutorStub(arg1, arg2)
	}
	if specificReturn {
		return ret.result1
	}
	fakeReturns := fake.txQueryExecutorReturns
	return fakeReturns.result1
}

func (fake *QueryExecutorProvider) TxQueryExecutorCallCount() int {
	fake.txQueryExecutorMutex.RLock()
	defer fake.txQueryExecutorMutex.RUnlock()
	return len(fake.txQueryExecutorArgsForCall)
}

func (fake *QueryExecutorProvider) TxQueryExecutorCalls(stub func(string, string) ledger.SimpleQueryExecutor) {
	fake.txQueryExecutorMutex.Lock()
	defer fake.txQueryExecutorMutex.Unlock()
	fake.TxQueryExecutorStub = stub
}

func (fake *QueryExecutorProvider) TxQueryExecutorArgsForCall(i int) (string, string) {
	fake.txQueryExecutorMutex.RLock()
	defer fake.txQueryExecutorMutex.RUnlock()
	argsForCall := fake.txQueryExecutorArgsForCall[i]
	return argsForCall.arg1, argsForCall.arg2
}

func (fake *QueryExecutorProvider) TxQueryExecutorReturns(result1 ledger.SimpleQueryExecutor) {
	fake.txQueryExecutorMutex.Lock()
	defer fake.txQueryExecutorMutex.Unlock()
	fake.TxQueryExecutorStub = nil
	fake.txQueryExecutorReturns = struct {
		result1 ledger.SimpleQueryExecutor
	}{result1}
}

func (fake *QueryExecutorProvider) TxQueryExecutorReturnsOnCall(i int, result1 ledger.SimpleQueryExecutor) {
	fake.txQueryExecutorMutex.Lock()
	defer fake.txQueryExecutorMutex.Unlock()
	fake.TxQueryExecutorStub = nil
	if fake.txQueryExecutorReturnsOnCall == nil {
		fake.txQueryExecutorReturnsOnCall = make(map[int]struct {
			result1 ledger.SimpleQueryExecutor
		})
	}
	fake.txQueryExecutorReturnsOnCall[i] = struct {
		result1 ledger.SimpleQueryExecutor
	}{result1}
}

func (fake *QueryExecutorProvider) Invocations() map[string][][]interface{} {
	fake.invocationsMutex.RLock()
	defer fake.invocationsMutex.RUnlock()
	fake.txQueryExecutorMutex.RLock()
	defer fake.txQueryExecutorMutex.RUnlock()
	copiedInvocations := map[string][][]interface{}{}
	for key, value := range fake.invocations {
		copiedInvocations[key] = value
	}
	return copiedInvocations
}

func (fake *QueryExecutorProvider) recordInvocation(key string, args []interface{}) {
	fake.invocationsMutex.Lock()
	defer fake.invocationsMutex.Unlock()
	if fake.invocations == nil {
		fake.invocations = map[string][][]interface{}{}
	}
	if fake.invocations[key] == nil {
		fake.invocations[key] = [][]interface{}{}
	}
	fake.invocations[key] = append(fake.invocations[key], args)
}

var _ lifecycle.QueryExecutorProvider = new(QueryExecutorProvider)
