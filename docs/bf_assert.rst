.. _bf_assert:

bf_assert
+++++++++
Makes assertions about a Batfish snapshot

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Makes assertions about the contents and/or behavior of a Batfish snapshot.



Requirements
------------
The following software packages must be installed on hosts that execute this module:

* pybatfish



.. _module-specific-options-label:

Module-specific Options
-----------------------
The following options may be specified for this module:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>assertions<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>yes</td>
    <td></td>
    <td></td>
    <td>
        <div>List of assertions to make about the snapshot.</div>
    </td>
    </tr>

    <tr>
    <td>network<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>Name of the network to make assertions about. This defaults to the value in the <code>bf_network</code> fact.</div>
    </td>
    </tr>

    <tr>
    <td>session<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>Batfish session parameters required to connect to the Batfish service. This defaults to the value in <code>bf_session</code> fact.</div>
    </td>
    </tr>

    <tr>
    <td>snapshot<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>Name of the snapshot to make assertions about. This defaults to the value in the <code>bf_snapshot</code> fact.</div>
    </td>
    </tr>

    </table>
    </br>

.. _bf_assert-examples-label:

Examples
--------

::

    
    # Confirm there are no undefined references or incompatible BGP sessions
    - bf_assert:
        assertions:
          - type: assert_no_undefined_references
            name: Confirm we have no undefined references
          - type: assert_no_incompatible_bgp_sessions
            name: Confirm we have no incompatible BGP sessions

    # Confirm 10.10.10.10 is reachable by traffic entering Gig0/0 of as1border1
    - bf_assert:
        assertions:
          - type: assert_reachable
            name: confirm host is reachable for traffic received on GigEth0/0
            parameters:
              startLocation: '@enter(as1border1[GigabitEthernet0/0])'
              headers:
                dstIps: '10.10.10.10'

    # Confirm a filter denies some specific traffic
    - bf_assert:
        assertions:
          - type: assert_filter_denies
            name: confirm node1 filter block_access denies TCP traffic on port 22
            parameters:
              filter_name: 'node1["block_access"]'
              headers:
                applications: 'ssh'



Return Values
-------------

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>


    <tr>
    <td>result</td>
    <td>
        <div>List of assertion results.</div>
    </td>
    <td align=center>always</td>
    <td align=center>list</td>
    <td align=center></td>
    </tr>

    <tr>
    <td>summary</td>
    <td>
        <div>Summary of action(s) performed.</div>
    </td>
    <td align=center>always</td>
    <td align=center>str</td>
    <td align=center></td>
    </tr>

    </table>
    </br>
    </br>





Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


