import pytest

import copy


@pytest.fixture(autouse=True, scope="module")
def gas_proxy_config(populus_config):
    populus_config.deploy_constructor_args = {
        'GasProxy': lambda dc: (dc['GasProxyTester']._meta.blockchain_client.get_coinbase(), dc['GasProxyTester']._meta.address),
    }
    populus_config.deploy_dependencies = {
        'GasProxy': {'GasProxyTester'},
    }


@pytest.fixture(scope="module")
def gas_proxy(deployed_contracts):
    _gas_proxy = deployed_contracts.GasProxy
    tester = deployed_contracts.GasProxyTester

    proxy_functions = {f.name: copy.copy(f) for f in tester._config._functions}
    for f in proxy_functions.values():
        f._bind(_gas_proxy)

    _gas_proxy.__dict__.update(proxy_functions)
    return _gas_proxy
