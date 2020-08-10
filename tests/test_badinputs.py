# -*- coding: utf-8 -*-
import os
import sys

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(CURRENT_DIRECTORY)
sys.path.append(os.path.dirname(CURRENT_DIRECTORY))

import time
import pytest
import helics as h

from test_init import createBroker, createValueFederate, destroyFederate, destroyBroker, createMessageFederate
import pytest as pt
import sys


def test_bad_input_message_federate_message():
    broker = createBroker(1)
    mFed1, fedinfo = createMessageFederate(1, "test")

    ept1 = h.helicsFederateRegisterGlobalEndpoint(mFed1, "ept1", "")
    # pytests.expect_exception(h.helicsFederateRegisterGlobalEndpoint(mFed1, "ept1", ""))

    h.helicsFederateEnterExecutingMode(mFed1)
    h.helicsEndpointSetDefaultDestination(ept1, "ept1")

    mess0 = h.helicsEndpointGetMessage(ept1)
    assert mess0.length == 0

    mess0 = h.helicsFederateGetMessage(mFed1)
    assert mess0.length == 0

    h.helicsEndpointSendMessage(ept1, mess0)

    h.helicsFederateRequestNextStep(mFed1)
    cnt = h.helicsEndpointPendingMessages(ept1)
    assert cnt == 1

    h.helicsFederateFinalize(mFed1)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsEndpointSendMessage(ept1, mess0)

    destroyFederate(mFed1, fedinfo)
    destroyBroker(broker)


def test_bad_input_filter_test4():

    broker = createBroker(1)
    mFed1, fedinfo = createMessageFederate(1, "test")

    filt1 = h.helicsFederateRegisterCloningFilter(mFed1, "filt1")
    # @test_throws h.HELICSErrorRegistrationFailure filt2 = h.helicsFederateRegisterCloningFilter(mFed1, "filt1")

    # @test_throws h.HELICSErrorInvalidArgument h.helicsFilterSetString(filt1, "unknown", "string")

    h.helicsFederateRegisterGlobalEndpoint(mFed1, "ept1", "")

    h.helicsFilterAddDeliveryEndpoint(filt1, "ept1")
    h.helicsFilterAddSourceTarget(filt1, "ept1")
    h.helicsFilterAddDestinationTarget(filt1, "ept1")
    h.helicsFilterRemoveTarget(filt1, "ept1")

    # @test_throws h.HELICSErrorInvalidArgument h.helicsFilterSet(filt1, "unknown", 10.0)
    h.helicsFederateFinalize(mFed1)

    destroyFederate(mFed1, fedinfo)
    destroyBroker(broker)


def test_bad_input_filter_core_tests():

    broker = createBroker(1)
    mFed1, fedinfo = createMessageFederate(1, "test")

    cr = h.helicsFederateGetCoreObject(mFed1)

    filt1 = h.helicsCoreRegisterFilter(cr, h.HELICS_FILTER_TYPE_DELAY, "filt1")
    # @test_throws h.HELICSErrorRegistrationFailure filt2 = h.helicsCoreRegisterFilter(cr, h.HELICS_FILTER_TYPE_DELAY, "filt1")
    h.helicsFilterSetOption(filt1, h.HELICS_HANDLE_OPTION_CONNECTION_OPTIONAL, True)
    assert h.helicsFilterGetOption(filt1, h.HELICS_HANDLE_OPTION_CONNECTION_OPTIONAL)
    h.helicsFederateFinalize(mFed1)
    h.helicsCoreDestroy(cr)

    destroyFederate(mFed1, fedinfo)
    destroyBroker(broker)


def test_bad_input_type_publication_2_tests():
    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "test")

    pubid = h.helicsFederateRegisterGlobalTypePublication(vFed1, "pub1", "string", "")
    # @test_throws h.HELICSErrorRegistrationFailure pubid2 = h.helicsFederateRegisterGlobalTypePublication(vFed1, "pub1", "string", "")

    # @test_throws h.HELICSErrorInvalidArgument h.helicsFederateRegisterFromPublicationJSON(vFed1, "unknownfile.json")

    # @test_throws h.HELICSErrorExternalType h.helicsFederateRegisterInterfaces(vFed1, "unknownfile.json")

    subid = h.helicsFederateRegisterTypeInput(vFed1, "inp1", "string", "")
    # @test_throws h.HELICSErrorRegistrationFailure subid2 = h.helicsFederateRegisterTypeInput(vFed1, "inp1", "string", "")

    h.helicsInputAddTarget(subid, "pub1")

    h.helicsFederateSetTimeProperty(vFed1, h.HELICS_PROPERTY_TIME_PERIOD, 1.0)

    h.helicsFederateEnterExecutingModeIterativeAsync(vFed1, h.HELICS_ITERATION_REQUEST_NO_ITERATION)
    res = h.helicsFederateEnterExecutingModeIterativeComplete(vFed1)
    assert res == h.HELICS_ITERATION_RESULT_NEXT_STEP

    h.helicsPublicationPublishTime(pubid, 27.0)

    # @test_throws h.HELICSErrorInvalidArgument h.helicsFederatePublishJSON(vFed1, "unknownfile.json")

    h.helicsFederateRequestNextStep(vFed1)
    str = h.helicsInputGetString(subid)
    assert str[0] == "2"
    assert str[1] == "7"
    h.helicsFederateClearUpdates(vFed1)

    h.helicsFederateFinalize(vFed1)

    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishRaw(pubid, str)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishString(pubid, str)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishInteger(pubid, 5)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishBoolean(pubid, True)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishDouble(pubid, 39.2)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishTime(pubid, 19.2)
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishChar(pubid, 'a')

    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishComplex(pubid, 2.5 + -9.8im)

    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishVector(pubid, [1.3, 2.9])

    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsPublicationPublishNamedPoint(pubid, "hello world", 2.0)

    destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_input_tests_raw_tests():

    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "test")

    pubid = h.helicsFederateRegisterPublication(vFed1, "pub1", h.HELICS_DATA_TYPE_RAW, "")

    subid = h.helicsFederateRegisterGlobalInput(vFed1, "inp1", h.HELICS_DATA_TYPE_RAW, "")

    h.helicsPublicationAddTarget(pubid, "inp1")

    h.helicsFederateSetTimeProperty(vFed1, h.HELICS_PROPERTY_TIME_PERIOD, 1.0)

    h.helicsFederateEnterExecutingMode(vFed1)

    h.helicsPublicationPublishDouble(pubid, 27.0)
    h.helicsFederateRequestNextStep(vFed1)
    h.helicsInputGetRawValue(subid)

    s = h.helicsInputGetString(subid)
    assert s == "0.000000"
    val = h.helicsInputGetComplexObject(subid)
    assert val == 0.0 + 0.0j

    h.helicsFederateFinalize(vFed1)

    t, res = h.helicsFederateRequestTimeIterative(vFed1, 1.0, h.HELICS_ITERATION_REQUEST_NO_ITERATION)
    # TODO: how to get enum values?
    # assert res == h.HELICS_ITERATION_RESULT_HALTED

    destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_input_duplicate_publication_and_input_pathways():

    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")

    pubid = h.helicsFederateRegisterTypePublication(vFed1, "pub1", "string", "")

    # @test_throws h.HELICSErrorRegistrationFailure pubid2 = h.helicsFederateRegisterTypePublication(vFed1, "pub1", "string", "")

    subid = h.helicsFederateRegisterGlobalTypeInput(vFed1, "inp1", "string", "")
    # @test_throws h.HELICSErrorRegistrationFailure subid2 = h.helicsFederateRegisterGlobalTypeInput(vFed1, "inp1", "string", "")

    # @test_throws h.HELICSErrorInvalidObject ept = h.helicsFederateRegisterEndpoint(vFed1, "ept1", "")

    h.helicsInputAddTarget(subid, "Testfed0/pub1")

    h.helicsFederateSetTimeProperty(vFed1, h.HELICS_PROPERTY_TIME_PERIOD, 1.0)

    h.helicsFederateEnterExecutingMode(vFed1)

    h.helicsPublicationPublishDouble(pubid, 27.0)
    h.helicsFederateRequestNextStep(vFed1)
    str = h.helicsInputGetString(subid)
    assert str[0] == "2"
    assert str[1] == "7"

    messages = h.helicsFederatePendingMessages(vFed1)
    assert messages == 0

    h.helicsFederateFinalize(vFed1)

    destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_input_init_error():
    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")

    # register the publications

    # the types here don't match which causes an error when initializing the federation
    h.helicsFederateRegisterGlobalTypePublication(vFed1, "pub1", "custom1", "")

    subid = h.helicsFederateRegisterTypeInput(vFed1, "inp1", "custom2", "")
    k1 = h.helicsInputGetKey(subid)

    # check some other calls
    inp2 = h.helicsFederateGetInput(vFed1, "inp1")
    k2 = h.helicsInputGetKey(inp2)
    assert k1 == k2

    inp3 = h.helicsFederateGetInputByIndex(vFed1, 0)
    k3 = h.helicsInputGetKey(inp3)
    assert k1 == k3

    h.helicsInputAddTarget(subid, "pub1")

    h.helicsFederateSetTimeProperty(vFed1, h.HELICS_PROPERTY_TIME_PERIOD, 1.0)

    # unknown publication
    # @test_throws h.HELICSErrorInvalidArgument pub3 = h.helicsFederateGetPublication(vFed1, "unknown")

    # error in this call from the mismatch
    # @test_throws h.HELICSErrorConnectionFailure h.helicsFederateEnterInitializingMode(vFed1)

    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsFederateRequestTimeAdvance(vFed1, 0.1)

    # unknown input
    # @test_throws h.HELICSErrorInvalidArgument inp4 = h.helicsFederateGetInput(vFed1, "unknown")

    # invalid input index
    # TODO: does this test segfault some times?
    # @test_throws h.HELICSErrorInvalidArgument inp5 = h.helicsFederateGetInputByIndex(vFed1, 4)

    h.helicsFederateFinalize(vFed1)

    destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_inputs_input_tests():

    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")

    # register the publications

    pubid = h.helicsFederateRegisterGlobalPublication(vFed1, "pub1", h.HELICS_DATA_TYPE_DOUBLE, "")

    subid = h.helicsFederateRegisterInput(vFed1, "inp1", h.HELICS_DATA_TYPE_DOUBLE, "")
    # @test_throws h.HELICSErrorRegistrationFailure subid2 = h.helicsFederateRegisterInput(vFed1, "inp1", h.HELICS_DATA_TYPE_DOUBLE, "")

    h.helicsInputAddTarget(subid, "pub1")

    vf2 = h.helicsFederateClone(vFed1)
    assert h.helicsFederateGetName(vFed1) == h.helicsFederateGetName(vf2)

    h.helicsFederateSetTimeProperty(vFed1, h.HELICS_PROPERTY_TIME_PERIOD, 1.0)

    # @test_throws h.HELICSErrorInvalidObject ept = h.helicsFederateRegisterEndpoint(vFed1, "ept1", "")

    h.helicsFederateEnterInitializingMode(vFed1)

    h.helicsPublicationPublishDouble(pubid, 27.0)

    comp = h.helicsFederateEnterExecutingModeIterative(vFed1, h.HELICS_ITERATION_REQUEST_FORCE_ITERATION)
    assert comp == h.HELICS_ITERATION_RESULT_ITERATING
    val = h.helicsInputGetDouble(subid)
    assert val == 27.0
    valt = h.helicsInputGetTime(subid)
    assert valt == 27.0

    comp = h.helicsFederateEnterExecutingModeIterative(vFed1, h.HELICS_ITERATION_REQUEST_ITERATE_IF_NEEDED)

    assert comp == h.HELICS_ITERATION_RESULT_NEXT_STEP

    val2 = h.helicsInputGetDouble(subid)
    assert val2 == val
    # expect error entering initializing Mode again
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsFederateEnterInitializingMode(vFed1)

    # expect error entering initializing Mode again
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsFederateEnterInitializingModeAsync(vFed1)

    # expect error entering initializing Mode again
    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsFederateEnterInitializingModeComplete(vFed1)

    h.helicsFederateFinalize(vFed1)

    destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_inputs_core_link():
    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")

    # register the publications

    h.helicsFederateRegisterGlobalTypePublication(vFed1, "pub1", "custom1", "")

    h.helicsFederateRegisterTypeInput(vFed1, "inp1", "custom2", "")

    fed2 = h.helicsGetFederateByName(h.helicsFederateGetName(vFed1))
    assert h.helicsFederateGetName(fed2) == h.helicsFederateGetName(vFed1)

    # @test_throws h.HELICSErrorInvalidArgument fed3 = h.helicsGetFederateByName("fed_unknown")

    cr = h.helicsFederateGetCoreObject(vFed1)
    h.helicsCoreDataLink(cr, "pub1", "fed0/inp1")

    # @test_throws h.HELICSErrorInvalidArgument h.helicsCoreMakeConnections(cr, "unknownfile.json")

    # TODO: This test should throw an error
    # @test_throws h.HELICSErrorInvalidArgument h.helicsCoreDataLink(cr, "pub1", "")
    # @test_broken False

    cr2 = h.helicsCoreClone(cr)
    assert h.helicsCoreGetAddress(cr2) == h.helicsCoreGetAddress(cr)

    # TODO: this should error as well
    h.helicsFederateEnterExecutingMode(vFed1)
    # @test_broken False

    h.helicsFederateFinalize(vFed1)

    destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_inputs_broker_link():

    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")

    # register the publications

    h.helicsFederateRegisterGlobalTypePublication(vFed1, "pub1", "custom1", "")

    h.helicsFederateRegisterTypeInput(vFed1, "inp1", "custom2", "")

    br = h.helicsBrokerClone(broker)

    h.helicsBrokerDataLink(br, "pub1", "Testfed0/inp1")

    # TODO: This test should throw an error
    # @test_throws h.HELICSErrorInvalidArgument h.helicsBrokerDataLink(br, "pub1", "")
    # @test_broken False

    # @test_throws h.HELICSErrorInvalidArgument h.helicsBrokerMakeConnections(br, "unknownfile.json")

    # @test_throws h.HELICSErrorConnectionFailure h.helicsFederateEnterExecutingMode(vFed1)

    h.helicsFederateFinalize(vFed1)

    destroyFederate(vFed1, fedinfo)

    h.helicsBrokerWaitForDisconnect(broker, 200)

    destroyBroker(broker)


def test_bad_inputs_frees():
    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")

    fi = h.helicsCreateFederateInfo()
    h.helicsFederateInfoSetBroker(fi, "broker test")
    h.helicsFederateEnterInitializingMode(vFed1)
    h.helicsFederateFinalize(vFed1)

    h.helicsFederateInfoSetBrokerPort(fi, 8929)
    h.helicsFederateInfoSetLocalPort(fi, "8229")

    h.helicsFederateInfoFree(fi)
    h.helicsFederateFree(vFed1)

    # @test_throws h.HELICSErrorInvalidObject destroyFederate(vFed1, fedinfo)
    destroyBroker(broker)


def test_bad_inputs_init_error_5():

    broker = createBroker(1)
    vFed1, fedinfo = createValueFederate(1, "fed0")
    # register the publications

    h.helicsFederateInfoSetSeparator(fedinfo, "-")
    h.helicsFederateSetSeparator(vFed1, "-")

    h.helicsFederateRegisterGlobalTypePublication(vFed1, "pub1", "custom1", "")

    subid = h.helicsFederateRegisterTypeInput(vFed1, "inp1", "custom2", "")

    h.helicsInputAddTarget(subid, "pub1")

    h.helicsFederateSetTimeProperty(vFed1, h.HELICS_PROPERTY_TIME_PERIOD, 1.0)

    # @test_throws h.HELICSErrorConnectionFailure resIt = h.helicsFederateEnterExecutingModeIterative(vFed1, h.HELICS_ITERATION_REQUEST_NO_ITERATION);

    # @test_throws h.HELICSErrorInvalidFunctionCall h.helicsFederateRequestTimeIterativeAsync(vFed1, 1.0, h.HELICS_ITERATION_REQUEST_NO_ITERATION);

    # @test_throws h.HELICSErrorInvalidFunctionCall res = h.helicsFederateRequestTimeIterativeComplete(vFed1)

    h.helicsFederateFinalize(vFed1)

    destroyFederate(vFed1, fedinfo)

    destroyBroker(broker)


def test_bad_inputs_misc_tests():

    assert h.helicsGetPropertyIndex("") == -1
    assert h.helicsGetPropertyIndex("not_a_property") == -1

    assert h.helicsGetOptionIndex("") == -1
    assert h.helicsGetOptionIndex("not_a_property") == -1
