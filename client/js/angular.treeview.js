/*
    @license Angular Treeview version 0.1.6
    ⓒ 2013 AHN JAE-HA http://github.com/eu81273/angular.treeview
    License: MIT
    [TREE attribute]
    angular-treeview: the treeview directive
    tree-id : each tree's unique id.
    tree-model : the tree model on $scope.
    node-id : each node's id
    node-label : each node's label
    node-children: each node's children
    <div
        data-angular-treeview="true"
        data-tree-id="tree"
        data-tree-model="roleList"
        data-node-id="roleId"
        data-node-label="roleName"
        data-node-children="children" >
    </div>
*/

(function ( angular ) {
    'use strict';
    // var optimateApp = angular.module( 'angularTreeview', [] );

    // Add the right click directive
    // optimateApp.directive(
    angular.module( 'angularTreeview', [] )
    // .directive(
    //     'ngRightClick', function($parse)
    //         {
    //         return function(scope, element, attrs) {
    //             var fn = $parse(attrs.ngRightClick);
    //             element.bind('contextmenu', function(event) {
    //                 scope.$apply(function() {
    //                     event.preventDefault();
    //                     fn(scope, {$event:event});
    //                 });
    //             });
    //         };
    //     }
    // )

    // Add the treeview directive
    // optimateApp.directive(
    .directive(
        'treeModel', ['$compile', '$http', function( $compile, $http ) {
            return {
                restrict: 'A',
                link: function ( scope, element, attrs ) {
                    //tree id
                    var treeId = attrs.treeId;

                    //tree model
                    var treeModel = attrs.treeModel;

                    //node id
                    var nodeId = attrs.nodeId || 'id';

                    //node label
                    var nodeLabel = attrs.nodeLabel || 'label';

                    //children
                    var nodeChildren = attrs.nodeChildren || 'children';

                    //tree template
                    var template =
                        '<ul>' +
                            '<li data-ng-repeat="node in ' + treeModel + '">' +
                                '<i class="collapsed" data-ng-show="node.' + nodeChildren + '.length && node.collapsed" data-ng-click="' + treeId + '.selectNodeHead(node)"></i>' +
                                '<i class="expanded" data-ng-show="node.' + nodeChildren + '.length && !node.collapsed" data-ng-click="' + treeId + '.selectNodeHead(node)"></i>' +
                                '<i class="normal" data-ng-hide="node.' + nodeChildren + '.length"></i> ' +
                                '<span data-ng-class="node.selected" data-ng-click="' + treeId + '.selectNodeLabel(node)">{{node.' + nodeLabel + '}}</span>' +
                                '<div data-ng-hide="node.collapsed" data-tree-id="' + treeId + '" data-tree-model="node.' + nodeChildren + '" data-node-id=' + nodeId + ' data-node-label=' + nodeLabel + ' data-node-children=' + nodeChildren + '></div>' +
                            '</li>' +
                        '</ul>' +
                        '<div class="menu-bar">'+
                              '<ul>'+
                               ' <li>'+
                                  '<p>+</p>'+
                                  '<ul>'+
                                   ' <li>'+
                                        '<p>Add<p>'+
                                        '<p>Edit</p>'+
                                        '<p>Delete</p>'+
                                        '<p>Copy</p>'+
                                    '</li>'+
                                 ' </ul>'+
                                '</li>'+
                              '</ul>'+
                            '</div>';


                    //check tree id, tree model
                    if( treeId && treeModel ) {
                        //root node
                        if( attrs.angularTreeview ) {
                            //create tree object if not exists
                            scope[treeId] = scope[treeId] || {};

                            //if node head clicks,
                            scope[treeId].selectNodeHead = scope[treeId].selectNodeHead || function( selectedNode ){
                                //Collapse or Expand
                                selectedNode.collapsed = !selectedNode.collapsed;
                            };

                            // if node label right clicks
                            // scope[treeId].selectNodeLabel = scope[treeId].selectNodeLabelRightClicked || function( selectedNode ){
                            //     alert("Label right clicked");
                            // }

                            //if node label clicks,
                            scope[treeId].selectNodeLabel = scope[treeId].selectNodeLabel || function( selectedNode ){
                                //remove highlight from previous node
                                if( scope[treeId].currentNode && scope[treeId].currentNode.selected ) {
                                    scope[treeId].currentNode.selected = undefined;
                                }

                                //set highlight to selected node
                                selectedNode.selected = 'selected';
                                console.log("Node clicked");

                                //set currentNode
                                scope[treeId].currentNode = selectedNode;

                                // get the url path from the node and it's parent
                                var path = "";
                                // Get path
                                if (scope[treeId].currentNode.Parent == "0"){
                                    path = scope[treeId].currentNode.ID;
                                }
                                else{
                                    path =  scope[treeId].currentNode.Parent + "/" + scope[treeId].currentNode.ID;
                                }

                                // get path from parentid in node
                                // and go to that path with http
                                console.log ("Sending http request");
                                $http.get('http://127.0.0.1:8080/'+path).success
                                    (
                                    function(data)
                                        {
                                            console.log("Htpp request success: "+ data);
                                             // Append the response data to the subitem (chilren) of the current node
                                            scope[treeId].currentNode.Subitem =  data;
                                        }
                                    );
                            };
                        }
                        //Rendering template.
                        element.html('').append( $compile( template )( scope ) );

                        console.log("rendering complete");
                        console.log(scope[treeId]);
                    }
                }
            };
    }]);
})( angular );
