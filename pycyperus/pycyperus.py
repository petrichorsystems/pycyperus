''' pycyperus.py
This file is a part of 'pycyperus'
This program is free software: you can redistribute it and/or modify
hit under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'pycyperus' is a python api for cyperus-server

Copyright 2024 murray foster '''

#! /usr/bin/python3

import json
import queue
import sys
import threading
import time
import types
import uuid

from pythonosc.dispatcher import Dispatcher as OscDispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from pycyperus import errors
from pycyperus import exceptions


class _Server():
    def __init__(self, port, submitted_requests, response_queue):
        self.port = port
        self.submitted_requests = submitted_requests
        self.responses = response_queue
        self.server = None
        self.server_exc = None
        self.server_thread = threading.Thread(
            target=self.server_thread_run,
            args=(),
            daemon=True)
        self.server_thread.start()
        while not self.server and self.server_exc == None:
            time.sleep(0.001)
        if not self.server:
            return None

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        
    def server_thread_run(self):
        self.dispatcher = OscDispatcher()
        self.dispatcher.map('/cyperus/dsp/load', self.osc_dsp_load_handler)
        self.dispatcher.map('/cyperus/address', self.osc_address_handler)
        self.dispatcher.map('/cyperus/list/osc/client', self.osc_list_osc_client_handler)
        self.dispatcher.map('/cyperus/add/osc/client', self.osc_add_osc_client_handler)                
        self.dispatcher.map('/cyperus/list/main', self.osc_list_main_handler)
        self.dispatcher.map('/cyperus/list/bus', self.osc_list_bus)
        self.dispatcher.map('/cyperus/list/bus_port', self.osc_list_bus_port)
        self.dispatcher.map('/cyperus/add/bus', self.osc_add_bus)
        self.dispatcher.map('/cyperus/add/connection', self.osc_add_connection)
        self.dispatcher.map('/cyperus/remove/connection', self.osc_remove_connection)
        self.dispatcher.map('/cyperus/list/module', self.osc_list_module)
        self.dispatcher.map('/cyperus/list/module_port', self.osc_list_module_port)
        self.dispatcher.map('/cyperus/get/system/env_variable', self.osc_get_system_env_variable)
        self.dispatcher.map('/cyperus/add/module/oscillator/sine', self.osc_add_module_oscillator_sine)
        self.dispatcher.map('/cyperus/add/module/envelope/follower', self.osc_add_module_envelope_follower)        
        try:
            self.server = osc_server.ThreadingOSCUDPServer(
                ('127.0.0.1', self.port), self.dispatcher)
        except OSError as exc:
            self.server_exc = exc
            return

        self.server.serve_forever()
        
    def osc_dsp_load_handler(self,
                             path,
                             dsp_cpu_load):
        return
        
    def osc_address_handler(self,
                            path,
                            request_id,
                            errno,
                            multipart,
                            new_host_out,
                            new_port_out):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/address'")
        args = (errno, multipart, new_host_out, new_port_out)
        self.responses[request_id] = args

    def osc_list_osc_client_handler(self,
                              path,
                              request_id,
                              errno,
                              multipart,
                              clients_str):
        if request_id not in self.submitted_requests:
            return
        print("received '/cyperus/list/osc/client'")
        args = (errno,
                multipart,
                clients_str)
        self.responses[request_id] = args

    def osc_add_osc_client_handler(self,
                              path,
                              request_id,
                              errno,
                              multipart):
        if request_id not in self.submitted_requests:
            return
        print("received '/cyperus/add/osc/client'")
        args = (errno,
                multipart)
        self.responses[request_id] = args
        
    def osc_list_main_handler(self,
                              path,
                              request_id,
                              errno,
                              multipart,
                              mains_str):
        if request_id not in self.submitted_requests:
            return
        print("received '/cyperus/list/main'")        
        args = (errno,
                multipart,
                mains_str)
        self.responses[request_id] = args

    def osc_list_bus(self,
                     path,
                     request_id,
                     errno,
                     multipart,
                     bus_id,
                     list_type,
                     result_str):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/list/bus'")
        args = (errno,
                multipart,
                bus_id,
                list_type,
                result_str)
        self.responses[request_id] = args

    def osc_list_bus_port(self,
                          path,
                          request_id,
                          errno,
                          multipart,
                          bus_id,
                          result_str):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/list/bus_port'")
        args = (errno,
                multipart,
                bus_id,
                result_str)
        self.responses[request_id] = args

    def osc_add_bus(self,
                    path,
                    request_id,
                    errno,
                    multipart,
                    target_bus_id,
                    bus_str,
                    ins_str,
                    outs_str,
                    new_id):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/add/bus'")
        args = (errno,
                multipart,
                target_bus_id,
                bus_str,
                ins_str,
                outs_str,
                new_id)
        self.responses[request_id] = args

    def osc_add_connection(self,
                           path,
                           request_id,
                           errno,
                           multipart,
                           port_out_id,
                           port_in_id,
                           new_connection_id):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/add/connection'")
        args = (errno,
                multipart,
                port_out_id,
                port_in_id,
                new_connection_id)
        self.responses[request_id] = args

    def osc_remove_connection(self,
                              path,
                              request_id,
                              errno,
                              multipart,
                              connection_id):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/remove/connection'")
        args = (errno,
                multipart,
                connection_id)
        self.responses[request_id] = args

    def osc_list_module(self,
                        path,
                        request_id,
                        errno,
                        multipart,
                        result_str):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/list/module'")
        args = (errno,
                multipart,
                result_str)
        self.responses[request_id] = args

    def osc_list_module_port(self,
                             path,
                             request_id,
                             errno,
                             multipart,
                             module_id,
                             result_str):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/list/module_port'")
        args = (errno,
                multipart,
                module_id,
                result_str)
        self.responses[request_id] = args

    def osc_get_system_env_variable(self,
                                    path,
                                    request_id,
                                    errno,
                                    multipart,
                                    var_name,
                                    env_variable):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/get/system/env_variable'")
        args = (errno,
                multipart,
                var_name,
                env_variable)
        self.responses[request_id] = args
        
    def osc_add_module_oscillator_sine(self,
                                       path,
                                       request_id,
                                       errno,
                                       multipart,
                                       module_id,
                                       frequency,
                                       amplitude,
                                       phase):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/add/module/oscillator/sine'")
        args = (errno,
                multipart,
                module_id,
                frequency,
                amplitude,
                phase)
        self.responses[request_id] = args

    def osc_add_module_envelope_follower(self,
                                         path,
                                         request_id,
                                         errno,
                                         multipart,
                                         module_id,
                                         attack,
                                         decay,
                                         scale):
        if request_id not in self.submitted_requests:
            return        
        print("received '/cyperus/add/module/oscillator/sine'")
        args = (errno,
                multipart,
                module_id,
                attack,
                decay,
                scale)
        self.responses[request_id] = args

class _Client():
    def __init__(self, port, submitted_requests, response_queue):
        self.client = udp_client.SimpleUDPClient('127.0.0.1', port)
        self.submitted_requests = submitted_requests
        self.responses = response_queue

    def _request(self, path, *data, fields=None):
        request_id = f"{uuid.uuid4()}"
        self.submitted_requests.add(request_id)
        data = (request_id,) + data
        self.client.send_message(path, data)        
        return request_id

    def _get_response_blocking(self, request_id, timeout=20):
        timeout_count = 0
        response = None
        timeout *= 1000
        while request_id not in self.responses and timeout_count < timeout:
            time.sleep(0.001)
            if timeout > 0:
                timeout_count += 1
        response = self.responses[request_id]
        if response:
            del self.responses[request_id]
            self.submitted_requests.remove(request_id)
        return response
    
    def _get_response_nonblocking(self, request_id):
        response = self.responses.get(request_id, None)
        if response:
            del self.responses[request_id]
            self.submitted_requests.remove(request_id)
        return response

    def list_osc_client(self, blocking=True):
        request_id = self._request("/cyperus/list/osc/client")

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None            

        clients = []
        for client_addr in filter(None, response[-1].split('\n')):
            client_id, ip, port, listener_enable = client_addr.split('|')
            print('listener_enable', listener_enable)
            print('listener_enable', bool(int(listener_enable)))            
            clients.append({
                'id': int(client_id),
                'ip': ip,
                'port': port,
                'listener_enable': bool(int(listener_enable))
            })
        return clients

    def add_osc_client(self, ip, port, listener_enable, blocking=True):
        request_id = self._request("/cyperus/add/osc/client",
                                   ip,
                                   port,
                                   listener_enable,
                                   "ssb")
        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None

        if response[0] == 0:
            return True
        return False

    
    def list_main(self, blocking=True):
        request_id = self._request("/cyperus/list/main")

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None            
        
        mains = {'in': [],
                 'out': []}
        raw_mains = response[-1].split('\n')
        outs = False
        for elem in filter(None, raw_mains):
            if elem in 'out:':
                outs = True
            elif elem in 'in:':
                pass
            elif outs:
                mains['out'].append(elem)
            else:
                mains['in'].append(elem)
        return mains

    def list_bus(self, bus_id, list_type, blocking=True):
        request_id = self._request(
            "/cyperus/list/bus",
            bus_id,
            list_type,
            'si'
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
            
        errno = response[1]
        if errno == errors.Cyperus.E_BUS_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target bus does not exist",
                [
                    exceptions.BusNotFound(),
                    exceptions.CyperusException()
                ]
            )
        
        bus_list = []
        for bus in list(filter(None, response[-1].split('\n'))):
            bus_id, name, ins_count, outs_count = bus.split('|')
            bus_list.append({
                'id': bus_id,
                'name': name,
                'ins_count': ins_count,
                'outs_count': outs_count
            })
        return bus_list

    def list_bus_port(self, bus_id, blocking=True):
        request_id = self._request(
            "/cyperus/list/bus_port",
            bus_id,
            's'
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
            
        errno = response[1]
        if errno == errors.Cyperus.E_BUS_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target bus does not exist",
                [
                    exceptions.BusNotFound(),
                    exceptions.CyperusException()
                ]
            )
        
        bus_ports = {'in': [],
                 'out': []}
        raw_bus_ports = response[-1].split('\n')
        outs = False
        for elem in filter(None, raw_bus_ports):
            if elem in 'out:':
                outs = True
            elif elem in 'in:':
                pass
            elif outs:
                bus_port_id, name = elem.split('|')
                bus_ports['out'].append({
                    'id': bus_port_id,
                    'name': name
                })
            else:
                bus_port_id, name = elem.split('|')
                bus_ports['in'].append({
                    'id': bus_port_id,
                    'name': name
                })
        return bus_ports

    def add_bus(self, bus_id, name, in_names, out_names, blocking=True):
        request_id = self._request(
            "/cyperus/add/bus",
            bus_id,
            name,
            in_names,
            out_names
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
        
        errno = response[1]
        if errno == errors.Cyperus.E_BUS_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target bus does not exist",
                [
                    exceptions.BusNotFound(),
                    exceptions.CyperusException()
                ]
            )
        
        return response[-1]

    def add_connection(self, port_id_out, port_id_in, blocking=True):
        request_id = self._request(
            "/cyperus/add/connection",
            port_id_out,
            port_id_in
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
        
        errno = response[1]
        if errno:
            if errno == errors.Cyperus.E_PORT_OUT_NOT_FOUND.value:
                raise ExceptionGroup(
                    "The target port out does not exist",
                    [
                        exceptions.PortOutNotFound(),
                        exceptions.CyperusException()
                    ]
                )
            if errno == errors.Cyperus.E_PORT_IN_NOT_FOUND.value:
                raise ExceptionGroup(
                    "The target port in does not exist",
                    [
                        exceptions.PortInNotFound(),
                        exceptions.CyperusException()
                    ]
                )
        
        return response[-1]

    def remove_connection(self, connection_id, blocking=True):
        request_id = self._request(
            "/cyperus/remove/connection",
            connection_id
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None        
        
        errno = response[1]
        if errno:
            if errno == errors.Cyperus.E_CONNECTION_NOT_FOUND.value:
                raise ExceptionGroup(
                    "The connection does not exist",
                    [
                        exceptions.ConnectionNotFound(),
                        exceptions.CyperusException()
                    ]
                )
        
        return response[-1]

    def list_module(self, bus_id, blocking=True):
        request_id = self._request(
            "/cyperus/list/module",
            bus_id,
            's'
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
        
        errno = response[1]
        if errno == errors.Cyperus.E_BUS_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target module does not exist",
                [
                    exceptions.BusNotFound(),
                    exceptions.CyperusException()
                ]
            )

        modules = []
        for module in list(filter(None, response[-1].split('\n'))):
            module_id, name = module.split('|')
            modules.append({
                'id': module_id,
                'name': name
            })
        return modules

    def list_module_port(self, module_id, blocking=True):
        request_id = self._request(
            "/cyperus/list/module_port",
            module_id,
            's'
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
        
        errno = response[1]
        if errno == errors.Cyperus.E_MODULE_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target module does not exist",
                [
                    exceptions.ModuleNotFound(),
                    exceptions.CyperusException()
                ]
            )
        
        module_ports = {'in': [],
                 'out': []}
        raw_module_ports = response[-1].split('\n')
        outs = False
        for elem in filter(None, raw_module_ports):
            if elem in 'out:':
                outs = True
            elif elem in 'in:':
                pass
            elif outs:
                module_port_id, name = elem.split('|')
                module_ports['out'].append({
                    'id': module_port_id,
                    'name': name
                })
            else:
                module_port_id, name = elem.split('|')
                module_ports['in'].append({
                    'id': module_port_id,
                    'name': name
                })
        return module_ports

    def get_system_env_variable(self, var_name, blocking=True):
        request_id = self._request(
            "/cyperus/get/system/env_variable",
            var_name
        )
        
        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)
            
        if not response:
            return None
            
        errno = response[1]
        if errno:
            raise Exception(f"{errno} found, error!")        
        return response[-1]
    
    def add_modules_oscillator_sine(self,
                                    bus_id,
                                    frequency,
                                    amplitude,
                                    phase,
                                    blocking=True):
        request_id = self._request(
            "/cyperus/add/module/oscillator/sine",
            bus_id,
            float(frequency),
            float(amplitude),
            float(phase)
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
        
        errno = response[1]
        if errno == errors.Cyperus.E_BUS_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target bus does not exist",
                [
                    exceptions.BusNotFound(),
                    exceptions.CyperusException()
                ]
            )
        return response[-4]

    def add_modules_envelope_follower(self,
                                      bus_id,
                                      attack,
                                      decay,
                                      scale,
                                      blocking=True):
        request_id = self._request(
            "/cyperus/add/module/envelope/follower",
            bus_id,
            float(attack),
            float(decay),
            float(scale)
        )

        if not blocking:
            response = self._get_response_nonblocking(request_id)
        else:
            response = self._get_response_blocking(request_id)

        if not response:
            return None
        
        errno = response[1]
        if errno == errors.Cyperus.E_BUS_NOT_FOUND.value:
            raise ExceptionGroup(
                "The target bus does not exist",
                [
                    exceptions.BusNotFound(),
                    exceptions.CyperusException()
                ]
            )
        return response[-4]    

    
class Api():
    def __init__(self, port_receive, port_send):
        self.port_receive = port_receive
        self.port_send = port_send
        self.submitted_requests = set()
        self.responses = {}        
        self.server = _Server(port_receive, self.submitted_requests, self.responses)
        if self.server.server_exc:
            raise self.server.server_exc
        else:
            self.client = _Client(port_send, self.submitted_requests, self.responses)

    def close(self):
        self.server.close()
        
    def list_main(self):
        return self.client.list_main()

    def list_osc_client(self):
        return self.client.list_osc_client()

    def add_osc_client(self, ip, port, listener_enable):
        return self.client.add_osc_client(str(ip), str(port), listener_enable)
    
    def list_bus(self, bus_id, list_type):
        LIST_TYPES = {
            'ADJACENT_PEER':     0,
            'ALL_PEERS':         1,
            'DIRECT_DESCENDANT': 2,
            'ALL_DESCENDANTS':   3
        }
        if bus_id == None:
            bus_id = ""
        if not list_type:
            raise ExceptionGroup(
                f"List type is missing, must be one of: {list(LIST_TYPES.keys())}",
                [
                    exceptions.MissingListType(),
                    exceptions.ApiException()
                ]
            )
        if list_type not in list(LIST_TYPES.keys()):
            raise ExceptionGroup(
                f"List type is invalid, must be one of: {list(LIST_TYPES.keys())}",
                [
                    exceptions.InvalidListType(),
                    exceptions.ApiException()
                ]
            )
        return self.client.list_bus(bus_id, LIST_TYPES[list_type])

    def list_bus_port(self, bus_id):
        if bus_id == None:
            raise ExceptionGroup(
                f"Missing bus ID",
                [
                    exceptions.MissingBusId(),
                    exceptions.ApiException()
                ]
            )
        if not bus_id:
            raise ExceptionGroup(
                f"Missing bus ID",
                [
                    exceptions.MissingBusId(),
                    exceptions.ApiException()
                ]
            )                
        return self.client.list_bus_port(bus_id)

    def add_bus(self, bus_id, bus_name, in_names, out_names):
        if bus_id == None:
            raise ExceptionGroup(
                f"Missing bus ID",
                [
                    exceptions.MissingBusId(),
                    exceptions.ApiException()
                ]
            )
        if not bus_name:
            raise ExceptionGroup(
                f"Missing bus name",
                [
                    exceptions.MissingBusName(),
                    exceptions.ApiException()
                ]
            )
        return self.client.add_bus(bus_id, bus_name, in_names, out_names)

    def add_connection(self, port_out_id, port_in_id):
        if not port_out_id:
            raise ExceptionGroup(
                f"Missing port out ID",
                [
                    exceptions.MissingPortOutId(),
                    exceptions.ApiException()
                ]
            )
        if not port_in_id:
            raise ExceptionGroup(
                f"Missing port in ID",
                [
                    exceptions.MissingPortInId(),
                    exceptions.ApiException()
                ]
            )        
        return self.client.add_connection(port_out_id, port_in_id)

    def remove_connection(self, connection_id):
        if not connection_id:
            raise ExceptionGroup(
                f"Missing connection ID",
                [
                    exceptions.MissingConnectionId(),
                    exceptions.ApiException()
                ]
            )        
        return self.client.remove_connection(connection_id)

    def list_module(self, bus_id):
        if not bus_id:
            raise ExceptionGroup(
                f"Missing bus ID",
                [
                    exceptions.MissingBusId(),
                    exceptions.ApiException()
                ]
            )        
        return self.client.list_module(bus_id)
    
    def list_module_port(self, module_id):
        if not module_id:
            raise ExceptionGroup(
                f"Missing module ID",
                [
                    exceptions.MissingModuleId(),
                    exceptions.ApiException()
                ]
            )        
        return self.client.list_module_port(module_id)

    def get_system_env_variable(self, var_name):
        return self.client.get_system_env_variable(var_name)
    
    def add_modules_oscillator_sine(self,
                                    bus_id,
                                    frequency,
                                    amplitude,
                                    phase):
        if not bus_id:
            raise ExceptionGroup(
                f"Missing bus ID",
                [
                    exceptions.MissingBusId(),
                    exceptions.ApiException()
                ]
            ) 
        return self.client.add_modules_oscillator_sine(bus_id,
                                                       float(frequency),
                                                       float(amplitude),
                                                       float(phase))

    def add_modules_envelope_follower(self,
                                      bus_id,
                                      attack,
                                      decay,
                                      scale):
        if not bus_id:
            raise ExceptionGroup(
                f"Missing bus ID",
                [
                    exceptions.MissingBusId(),
                    exceptions.ApiException()
                ]
            ) 
        return self.client.add_modules_envelope_follower(bus_id,
                                                         float(attack),
                                                         float(decay),
                                                         float(scale))
    
