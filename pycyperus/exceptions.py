''' exceptions.py
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

class ApiException(ValueError):
    def __init__(self, *args, **kwargs):
        """Initialize"""
        super().__init__(*args, **kwargs)    

class MissingListType(ApiException):
    """List type is missing"""

class InvalidListType(ApiException):
    """List type is invalid"""

class MissingBusId(ApiException):
    """Missing bus ID"""

class MissingBusName(ApiException):
    """Missing bus name"""

class MissingPortOutId(ApiException):
    """Missing port out ID"""

class MissingPortInId(ApiException):
    """Missing port in ID"""    

class MissingConnectionId(ApiException):
    """Missing connection ID"""

class MissingModuleParameterValue(ApiException):
    """Missing module parameter value"""
    
class RequestException(IOError):
    def __init__(self, *args, **kwargs):
        """Initialize"""
        super().__init__(*args, **kwargs)

class ResponseException(IOError):
    def __init__(self, *args, **kwargs):
        """Initialize"""
        super().__init__(*args, **kwargs)
        
class MalformedRequest(RequestException, ValueError):
    """The request is malformed"""
    
class MalformedResponse(ResponseException, ValueError):
    """The response is malformed"""

class MissingRequestID(MalformedRequest):
    """The request ID is missing"""

class MissingResponseErrorCode(MalformedResponse):
    """The response error code is missing"""

class MissingResponseMultipartFlag(MalformedResponse):
    """The response multipart flag is missing"""

class CyperusException(IOError):
    def __init__(self, *args, **kwargs):
        """Initialize"""
        super().__init__(*args, **kwargs)

class BusNotFound(CyperusException):
    """The target bus does not exist"""

class ConnectionNotFound(CyperusException):
    """The target connection does not exist"""
    
class PortOutNotFound(CyperusException):
    """The target port out does not exist"""

class PortInNotFound(CyperusException):
    """The target port in does not exist"""

class ModuleNotFound(CyperusException):
    """The target module does not exist"""
