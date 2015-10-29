def test_basic_call_relaying(deployed_contracts, gas_proxy):
    tester = deployed_contracts.GasProxyTester

    assert tester.flag() is False
    gas_proxy.doit()
    assert tester.flag() is True
    gas_proxy.undo()
    assert tester.flag() is False

    assert tester.value() == 0
    gas_proxy.set(12345)
    assert tester.value() == 12345
    gas_proxy.set(54321)
    assert tester.value() == 54321
