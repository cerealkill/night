pragma solidity ^0.4.11;

contract Ownable {

    address owner;

    function Ownable() {
        owner = msg.sender;
    }

    function kill() {
        if (msg.sender == owner) selfdestruct(owner);
    }
}

contract Device{

    struct Id {
        string manufacturer;
        string model;
        bytes32 serialNumber;
    }

    Id public deviceId;

    function Device(string _manufacturer, string _model, bytes32 _serialNumber) public {
        deviceId = Id({
            manufacturer: _manufacturer,
            model: _model,
            serialNumber: _serialNumber
        });
    }
}

contract DataLogger is Device, Ownable{

    struct LogEntry {
        uint timestamp;
        uint value;
    }

    LogEntry[] public registry;

    function DataLogger(string _manufacturer, string _model, bytes32 _serialNumber) Device( _manufacturer, _model, _serialNumber) public{}

    function log(uint _timestamp, uint _value){
        registry.push(LogEntry({
            timestamp: _timestamp,
            value: _value
        }));
    }


}