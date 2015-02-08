// Get all Optimate data with angular treeview using traversal
(function(){
  "use strict";
  var myApp = angular.module('myApp', ['angularTreeview']);
  myApp.controller('myController',
        ['$scope', '$http', function($scope, $http)
              {$http.get('http://127.0.0.1:8080').success
  	               (function(data)
  	                   {$scope.roleList = data;}
                      );

                   // Toggle if the modal dialog displays or not
                    $scope.modalShown = false;
                    $scope.toggleModal = function() {
                      console.log("shown: " + $scope.modalShown);
                    $scope.modalShown = !$scope.modalShown;
                     console.log("shown after: " + $scope.modalShown);
                  };
                  $scope.logClose = function() {
                      console.log('close!');
                      $scope.modalShown = false;
                    };
            }]
    );
})();
