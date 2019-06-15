Assertions supported by bf_assert module
++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 2

.. _assert_reachable:

assert_reachable
----------------
Assert that packets specified start locations and headers are successful



* This is an all-to-all reachability test. It will fail if any start location, header combination fails.


The following options may be specified for this assertion:

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
        <div>Constraints on packet headers. See <a href='...'>...</a> for header specification.</div>
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
Assert that packets specified start locations and headers do not succeed



* This is an all-to-all unreachability test. It will fail if any start location, header combination succeed.


The following options may be specified for this assertion:

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
        <div>Constraints on packet headers. See <a href='...'>...</a> for header specification.</div>
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


