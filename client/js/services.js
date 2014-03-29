'use strict';

/* Services */

function Connection($q, $log) {
    this.address = null;
    this._init = function() {
        this.connectPromiseFulfilled = false;
        this.connectPromise = $q.defer();
        this.updatePromise = $q.defer();
        this.connection = null;
    }.bind(this);
    this._init();

    this.isConnected = function() { return this.connectPromiseFulfilled; }

    this.connect = function(address) {
      $log.info("Connecting to", ['ws://', address].join(''));
      this.address = address;
      this.connection = new WebSocket(['ws://', address].join(''));
      this.connection.onopen = this.onopen;
      this.connection.onclose = this.onclose;
      this.connection.onmessage = this.onmessage;
      return this.connectPromise.promise;
    }.bind(this);

    this.getConnectPromise = function() {
      return this.connectPromise.promise;
    }.bind(this);

    this.getUpdatePromise = function() {
      return this.updatePromise.promise;
    }.bind(this);

    this.onopen = function() {
      $log.info('Connection established'); 
    };

    this.onclose = function(event) {
      $log.error('Connection closed:', event);
      this.updatePromise.reject(event);
      if (!this.connectPromiseFulfilled) {
        this.connectPromise.reject(event);
      }
      this._init();
    }.bind(this);

    this.onmessage = function(event) {
      $log.debug('Получены данные', event.data);
      var message = JSON.parse(event.data);
      if (!message || !message.type) {
        $log.error('Левое сообщение:', event.data);
        return;
      }

      if (message.type === 'table') {
        if(this.connectPromiseFulfilled) {
            $log.error('table сообщение повторилось');
            return;
        }
        this.connectPromiseFulfilled = true;
        $log.info('resolving');
        this.connectPromise.resolve(message.data);
      } else if (message.type === 'score') {
        this.updatePromise.notify(message.data);
      } else {
        $log.error('Неизвестный тип сообщения:', message.type);
      }

    }.bind(this);
}

var ncumcServices = angular.module('ncumcServices', []);

ncumcServices.factory('connection', ['$q', '$log',
  function($q, $log) {
    return new Connection($q, $log);
  }]);
