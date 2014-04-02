'use strict';

/* Controllers */

var ncumcControllers = angular.module('ncumcControllers', []);

ncumcControllers.controller('Welcome', ['$scope', '$log', '$location', '$timeout', 'connection',
  function($scope, $log, $location, $timeout, connection) {
    $scope.connecting = false;
    $scope.error = null;
    $scope.connectTimeout = null;

    $scope.connect = function() {
      $scope.error = null;
      $scope.connecting = true;
      $scope.connectTimeout && $timeout.cancel($scope.connectTimeout);
      connection.connect($scope.address)
        .then(function(table) {
           $location.url('/table'); 
        }, function(event) {
            if (!event.reason || event.reason === "") {
                $scope.error = "Can't connect";
            } else {
                $scope.error = event.reason;
            }
            $scope.connecting = false;
            $scope.setConnectTimeout();
        });
    };

    $scope.setConnectTimeout = function() {
      $log.debug('setting connect timeout');
      $scope.connectTimeout = $timeout($scope.connect, 10000);
    };

    $scope.addressChanged = function() {
      $log.debug('Address changed');
      $scope.error = null;
      $scope.connectTimeout && $timeout.cancel($scope.connectTimeout);
    };

    if (connection.address !== null) {
      $scope.address = connection.address;
      $scope.setConnectTimeout();
    }
  }]);

ncumcControllers.controller('Table', ['$scope', '$log', '$location', 'connection',
  function($scope, $log, $location, connection) {
    if (!connection.isConnected()) {
        $location.url('/');
    }
    connection.getConnectPromise().then(function(tableData) { $scope.data = tableData; });
    connection.getUpdatePromise().then(null, function() { $location.url('/welcome'); },
      function (scoreData) {
        for (var i = 0; i < $scope.data.length; i++) {
          if ($scope.data[i].id === scoreData.id) {
            $scope.data[i].score = Math.round( ($scope.data[i].score + scoreData.score) * 1000) / 1000;
            break;
          }
        }
      });
  }]);
