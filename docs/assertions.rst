Assertions supported by bf_assert module
++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 2

.. _assert_all_flows_fail:

assert_all_flows_fail
---------------------
Assert that all packets with specified start locations and headers fail



* This is an all-to-all test that analyzes all (start location, header) combinations
* If any flow (start location, header) can reach its destination, this assertion will return false.
* If no flow (start location, header) can reach its destination, this assertion will return true.
* This assertion is used to evaluate the security of select destinations in the network.


The following parameters may be specified for this assertion:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>headers<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Constraints on packet headers. See <a href='https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints'>https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints</a> for keys in this dictionary.</div>
    </td>
    </tr>

    <tr>
    <td>startLocation<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Start location specifier. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier</a> for location specification.</div>
    </td>
    </tr>

    </table>
    </br>


.. _assert_all_flows_succeed:

assert_all_flows_succeed
------------------------
Assert that all packets with specified start locations and headers are successful



* This is an all-to-all test that analyzes all (start location, header) combinations
* If any flow (start location, header) cannot reach its destination, this assertion will return false.
* If all flows (start location, header) can reach its destination, this assertion will return true.
* This assertion is used to evaluate the accessibility of select destinations in the network.


The following parameters may be specified for this assertion:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>headers<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Constraints on packet headers. See <a href='https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints'>https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints</a> for keys in this dictionary.</div>
    </td>
    </tr>

    <tr>
    <td>startLocation<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Start location specifier. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier</a> for location specification.</div>
    </td>
    </tr>

    </table>
    </br>


.. _assert_filter_has_no_unreachable_lines:

assert_filter_has_no_unreachable_lines
--------------------------------------
Assert that the filters (e.g., ACLs) have no unreachable lines



* A filter line is considered unreachable if it will never match a packet, e.g., because its match condition is empty or covered completely by those of prior lines.
* This test will fail if any line in any of the specified filter(s) is unreachable.


The following parameters may be specified for this assertion:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>filters<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Filter specifier. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier</a> for filter specification.</div>
    </td>
    </tr>

    </table>
    </br>


.. _assert_filter_denies:

assert_filter_denies
--------------------
Assert that the specified filters (e.g., ACLs) deny specified headers



* This test will fail if any packet in the specified header space is permitted by any of the specified filter(s).


The following parameters may be specified for this assertion:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>filters<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Filter specifier. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier</a> for filter specification.</div>
    </td>
    </tr>

    <tr>
    <td>headers<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Constraints on packet headers. See <a href='https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints'>https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints</a> for keys in this dictionary.</div>
    </td>
    </tr>

    </table>
    </br>


.. _assert_filter_permits:

assert_filter_permits
---------------------
Assert that the specified filters  (e.g., ACLs) permit specified headers



* This test will fail if any packet in the specified header space is denied by any of the specified filter(s).


The following parameters may be specified for this assertion:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>filters<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Filter specifier. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier</a> for filter specification.</div>
    </td>
    </tr>

    <tr>
    <td>headers<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Constraints on packet headers. See <a href='https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints'>https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints</a> for keys in this dictionary.</div>
    </td>
    </tr>

    </table>
    </br>


.. _assert_no_forwarding_loops:

assert_no_forwarding_loops
--------------------------
Assert that there are no forwarding loops



* This test will fail if any flow will experience a forwarding loop in the snapshot.
* This test takes no parameters.



.. _assert_no_incompatible_bgp_sessions:

assert_no_incompatible_bgp_sessions
-----------------------------------
Assert that all BGP sessions are compatibly configured



* This test finds all pairs of BGP session endpoints in the snapshot and will fail if the configuration of any pair is incompatible.
* This test takes no parameters.



.. _assert_no_unestablished_bgp_sessions:

assert_no_unestablished_bgp_sessions
------------------------------------
Assert that all compatibly-configured BGP sessions are established



* This test fails if there are any BGP session in the snapshot that are compatibly configured but will not be established (e.g., due to ACLs).
* This test takes no parameters.



.. _assert_no_undefined_references:

assert_no_undefined_references
------------------------------
Assert that there are no undefined references



* This test will fail if any device configuration refers to a structure (e.g., ACL, prefix-list, routemap) that is not defined in the configuration.
* This test takes no parameters.



