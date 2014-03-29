'use strict';

/* Controllers */

var ncumcControllers = angular.module('ncumcControllers', []);

ncumcControllers.controller('Welcome', ['$scope', '$log', '$location', 'connection',
  function($scope, $log, $location, connection) {
    $scope.connect = function() {
      $scope.connecting = true;
      $scope.error = null;
      connection.connect($scope.address)
        .then(function(table) {
           $location.url('/table'); 
        }, function(event) {
            $scope.error = {};
            if (!event.reason || event.reason === "") {
                $scope.error.reason = "Whatever!";
            } else {
                $scope.error.reason = event.reason;
            }
            $scope.connecting = false;
        });
    };
    if (connection.address !== null) {
      $scope.address = connection.address;
      $scope.connect();
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
