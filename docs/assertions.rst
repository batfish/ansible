Assertions supported by bf_assert module
++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 2

.. _assert_reachable:

assert_reachable
----------------
Assert that packets with specified start locations and headers are successful



* This is an all-to-all reachability test. It will fail if any (start location, header) combination fails.


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
    <td>start<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Start location specifier. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier</a> for location specification.</div>
    </td>
    </tr>

    </table>
    </br>


.. _assert_unreachable:

assert_unreachable
------------------
Assert that packets with specified start locations and headers do not succeed



* This is an all-to-all unreachability test. It will fail if any (start location, header) combination succeed.


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
    <td>start<br/><div style="font-size: small;"></div></td>
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
Assert that the filters (e.g., ACLs) have no unreachable lines.



* A filter line is considered unreachable if it will never match a packet, e.g., because its match condition is empty or covered completely by those of prior lines.
* This test will fail if any line in any filter is unreachable.


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
Assert that the specified filters (e.g., ACLs) deny specified headers.



* This test will fail if any packet in the specified header space is permitted by any filter.


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
Assert that the specified filters  (e.g., ACLs) permit specified headers.



* This test will fail if any packet in the specified header space is denied by any filter.


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


.. _assert_no_incompatible_bgp_sessions:

assert_no_incompatible_bgp_sessions
-----------------------------------
Assert that all BGP sessions are compatibly configured.



* This test finds all pairs of BGP session endpoints in the snapshot and will fail if the configuration of any pair is incompatible.
* This test takes no parameters.



.. _assert_no_undefined_references:

assert_no_undefined_references
------------------------------
Assert that there are no undefined references



* This test will fail if any device configuration refers to a structured (e.g., ACL or routemap) that is not defined in the configuration.
* This test takes no parameters.



