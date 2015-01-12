'use strict';

/* Controllers */

var costItems = angular.module('costItems', []);

costItems.controller('ItemListCtrl', ['$scope', '$http', function($scope, $http) {
    //$http.get('cost_items/cost_items.json').success(function(data) {
    $http.get('http://0.0.0.0:6543').success(function(data) {
    $scope.projects = data;
  });
}]);
