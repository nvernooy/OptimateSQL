// Function to get Optimate data without angular treeview module
/*'use strict'

var costItems = angular.module('costItems', []);

costItems.controller
('ItemListCtrl',
    [
        '$scope', '$http', function($scope, $http)
        {
            //$http.get('cost_items.json').success
            $http.get('http://127.0.0.1:8080').success
            (
                function(data)
                {
                $scope.projects = data;
                }
            );
        }
    ]
);*/

// Get all Optimate data with angular treeview
/*
(function(){
    "use strict";
  //angular module
  var myApp = angular.module('myApp', ['angularTreeview']);

  //test controller
  myApp.controller('myController',
        [
          '$scope', '$http', function($scope, $http)
              {
                    $http.get('http://127.0.0.1:8080').success
  	               (
  	                   function(data)
  	                   {
  	                       $scope.roleList = data;
                            }
                        );
              }
        ]
    );
})();
*/

// Return only the Project data
(function(){
    "use strict";
  //angular module
  var myApp = angular.module('myApp', ['angularTreeview']);

  //test controller
  myApp.controller('myController',
        [
          '$scope', '$http', function($scope, $http)
              {
                    $http.get('http://127.0.0.1:8080/projects').success
  	               (
  	                   function(data)
  	                   {
  	                       $scope.roleList = data;
                            }
                        );
              }
        ]
    );
})();


// Return the data of a specified Project
function project_data(project_id){
  "use strict";
  //angular module
  var projectdataApp = angular.module('projectdataApp', ['angularTreeview']);

  //test controller
  projectdataApp.controller('projectdataControl',
        [
          '$scope', '$http', function($scope, $http)
              {
                    $http.get('http://127.0.0.1:8080/project_data',
                                {
                                    headers: {'ProjectID': project_id}
                                }).success
  	               (
  	                   function(data)
  	                   {
  	                       $scope.roleList = data;
                            }
                        );
              }
        ]
    );
}

/*
	@license Angular Treeview version 0.1.6
	ⓒ 2013 AHN JAE-HA http://github.com/eu81273/angular.treeview
	License: MIT
*/
/*
(function(f){f.module("angularTreeview",[]).directive("treeModel",function($compile){return{restrict:"A",link:function(b,h,c){var a=c.treeId,g=c.treeModel,e=c.nodeLabel||"label",d=c.nodeChildren||"children",e='<ul><li data-ng-repeat="node in '+g+'"><i class="collapsed" data-ng-show="node.'+d+'.length && node.collapsed" data-ng-click="'+a+'.selectNodeHead(node)"></i><i class="expanded" data-ng-show="node.'+d+'.length && !node.collapsed" data-ng-click="'+a+'.selectNodeHead(node)"></i><i class="normal" data-ng-hide="node.'+
d+'.length"></i> <span data-ng-class="node.selected" data-ng-click="'+a+'.selectNodeLabel(node)">{{node.'+e+'}}</span><div data-ng-hide="node.collapsed" data-tree-id="'+a+'" data-tree-model="node.'+d+'" data-node-id='+(c.nodeId||"id")+" data-node-label="+e+" data-node-children="+d+"></div></li></ul>";a&&g&&(c.angularTreeview&&(b[a]=b[a]||{},b[a].selectNodeHead=b[a].selectNodeHead||function(a){a.collapsed=!a.collapsed},b[a].selectNodeLabel=b[a].selectNodeLabel||function(c){b[a].currentNode&&b[a].currentNode.selected&&
(b[a].currentNode.selected=void 0);c.selected="selected";b[a].currentNode=c}),h.html('').append($compile(e)(b)))}}})})(angular);
*/