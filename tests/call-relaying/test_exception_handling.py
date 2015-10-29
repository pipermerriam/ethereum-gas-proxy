from ethereum.utils import denoms


def test_function_throwing_exception(deploy_client, deployed_contracts, gas_proxy):
    deploy_client.send_transaction(to=gas_proxy._meta.address, value=10 * denoms.ether)

    before_balance = gas_proxy.get_balance()
    assert before_balance == 10 * denoms.ether

    txn_hash = gas_proxy.fails()
    txn = deploy_client.get_transaction_by_hash(txn_hash)
    txn_receipt = deploy_client.wait_for_transaction(txn_hash)

    gas_provided = int(txn['gas'], 16)
    gas_used = int(txn_receipt['gasUsed'], 16)

    assert gas_provided >= gas_used

    after_balance = gas_proxy.get_balance()

    gas_price = int(txn['gasPrice'], 16)
    gas_cost = gas_price * gas_used

    assert gas_cost > 0
    assert after_balance + gas_cost == before_balance
