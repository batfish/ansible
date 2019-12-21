.. _bf_session:

bf_session
++++++++++
Builds a session for use with other Batfish Ansible modules

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Builds a session for use with other Batfish Ansible modules and populates ``bf_session`` fact.



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
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>host<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Host (resolvable name or IP address) running the Batfish service.</div>
    </td>
    </tr>

    <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td>&quot;default&quot;</td>
    <td>
        <div>Name of the session.</div>
    </td>
    </tr>

    <tr>
    <td>parameters<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>no</td>
    <td>None</td>
    <td>
        <div>Dictionary with additional parameters used to configure the session. Use <code>{ssl: true}</code> to use SSL.</div>
    </td>
    </tr>

    </table>
    </br>

.. _bf_session-examples-label:

Examples
--------

::

    
    # Establish session with Batfish service running on localhost
    - bf_session:
        host: localhost
        name: my_session
    # Establish SSL session with Batfish service running at 10.10.10.10
    - bf_session:
        host: 10.10.10.10
        name: my_session
        parameters:
          ssl: true
    # Establish SSL session with Batfish Enterprise service running at 10.10.10.10
    - bf_session:
        host: 10.10.10.10
        name: enterprise_session
        parameters:
          ssl: true
          session_type: bfe



Return Values
-------------

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    </tr>


    <tr>
    <td>session</td>
    <td>
        <div>Details about the created session.</div>
    </td>
    <td align=center>always</td>
    <td align=center>complex</td>
    </tr>

    <tr>
    <td>contains:</td>
    <td colspan=4>
        <table border=1 cellpadding=2>

        <tr>
        <th class="head">name</th>
        <th class="head">description</th>
        <th class="head">returned</th>
        <th class="head">type</th>
        </tr>

        <tr>
        <td>host</td>
        <td>
            <div>Host where service is hosted</div>
        </td>
        <td align=center>always</td>
        <td align=center>str</td>
        </tr>

        <tr>
        <td>parameters</td>
        <td>
            <div>Additional parameters to connect to the service</div>
        </td>
        <td align=center>if supplied by user</td>
        <td align=center>dict</td>
        </tr>

        </table>
    </td>
    </tr>

    <tr>
    <td>summary</td>
    <td>
        <div>Summary of action(s) performed.</div>
    </td>
    <td align=center>always</td>
    <td align=center>str</td>
    </tr>

    </table>
    </br>
    </br>





Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


