'use strict';

/* App Module */

var ncumcApp = angular.module('ncumcApp', [
  'ngRoute',
  'ncumcControllers',
  'ncumcServices'
]);

ncumcApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/welcome', {
        templateUrl: 'partials/welcome.html',
        controller: 'Welcome'
      }).
      when('/table', {
        templateUrl: 'partials/table.html',
        controller: 'Table'
      }).
      otherwise({
        redirectTo: '/welcome'
      });
  }]);
