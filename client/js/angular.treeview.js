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
    .directive(
        'treeModel', ['$compile', '$http', function( $compile, $http) {
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
                    // path
                    var nodePath = attrs.nodePath || 'path'
                    // Copied node to be pasted
                    scope.copiednode;

                    //tree template
                    var template =
                        '<ul>' +
                            '<li data-ng-repeat="node in ' + treeModel + '">' +
                                '<i class="collapsed" ' +
                                    'data-ng-show="node.' + nodeChildren + '.length && node.collapsed" data-ng-click="' +
                                    treeId + '.selectNodeHead(node)">'+
                                '</i>' +
                                '<i class="expanded" '+
                                    'data-ng-show="node.' + nodeChildren + '.length && !node.collapsed" data-ng-click="' +
                                    treeId + '.selectNodeHead(node)">'+
                                '</i>' +
                                '<i class="normal" '+
                                    'data-ng-hide="node.' + nodeChildren + '.length">'+
                                '</i> ' +

                                // '<span class = "selectedNode" data-ng-class="node.selected" '+
                                //     'data-ng-click="' + treeId + '.selectNodeLabel(node)">{{node.' + nodeLabel + '}}'+
                                //     '<span class = "addItem">'+
                                //         '<a ng-click="addItem(node.'+nodePath+')" href="">+</a>'+
                                //     '</span>'
                                // '<span>' +

                                '<span data-ng-class="node.selected" '+
                                    'data-ng-click="' + treeId + '.selectNodeLabel(node)">{{node.' + nodeLabel + '}}'+
                                '</span>' +

                                '<span class="additem" ng-show="node.selected">'+
                                    '<button ng-click="toggleModal()">+</button>'+
                                                        '<modal-dialog show="modalShown" width="300px" height="50%">'+
                                                            '<button data-ng-click="' + treeId + '.addItem(node.Path)">Add</button>'+
                                                            '<button data-ng-click="' + treeId + '.deleteItem(node.Path, node.ID)">Delete</button>'+
                                                            '<button data-ng-click="' + treeId + '.copy(node.Path)">Copy</button>'+
                                                            '<button data-ng-click="' + treeId + '.paste(node.Path)">Paste</button>'+
                                                        '</modal-dialog>'+
                                '</span>'+

                                // Adding the "+" link add item
                                // '<span class="additem" ng-show="node.selected">'+
                                //     '<a data-ng-click="' + treeId + '.addItem(node.Path)" href="">+</a>'+
                                // '</span>'+

                                //Adding the "-" link delete item
                                // '<span class="deleteitem">'+
                                //     '<a data-ng-click="' + treeId + '.deleteItem(node.Path, node.ID)" href="">-</a>'+
                                // '</span>'+

                                // //Adding the "Copy" link to Copy item
                                // '<span class="copyitem">'+
                                //     '<a data-ng-click="' + treeId + '.copy(node.Path)" href="">Copy</a>'+
                                // '</span>'+

                                // //Adding the "Paste" link to Paste item
                                // '<span class="pasteitem">'+
                                //     '<a data-ng-click="' + treeId + '.paste(node.Path)" href="">Paste</a>'+
                                // '</span>'+

                                '<div data-ng-hide="node.collapsed" '+
                                    'data-tree-id="' + treeId +
                                    '" data-tree-model="node.' + nodeChildren +
                                    '" data-node-id=' + nodeId +
                                    ' data-node-label=' + nodeLabel +
                                    ' data-node-children=' + nodeChildren + '>'+
                                    ' data-node-path=' + nodePath + '>'+
                                '</div>' +

                            '</li>' +

                        '</ul>';


                    //check tree id, tree model
                    if( treeId && treeModel ) {
                        //root node
                        if( attrs.angularTreeview ) {
                            //create tree object if not exists
                            scope[treeId] = scope[treeId] || {};

                            // function to POST data to server to add item
                            scope[treeId].addItem = function(path) {
                                console.log("Adding data to: " +path);
                                $http({method: 'POST', url: 'http://localhost:8080' + path + 'add'}).success(
                                // $http({method: 'POST', url: 'http://localhost:8080/', data: {ID: itemId, Parent:parentid}}).success(
                                    function () {
                                        alert('Success: Child added');
                                    }
                                );
                            }

                            // Function to delete data in server
                              scope[treeId].deleteItem = function(path, id) {
                                        console.log("Deleteing " + id + " from " + path);
                                        // get parent path
                                        var temp = path.substring (0, path.length-1);
                                        console.log (temp)
                                        var parentpath = temp.substring(0, temp.lastIndexOf("/"));
                                        console.log (parentpath);
                                        $http({method: 'POST', url: 'http://localhost:8080' + parentpath + '/delete', data:{'ID': id}}).success(
                                        // $http({method: 'POST', url: 'http://localhost:8080/', data: {ID: itemId, Parent:parentid}}).success(
                                            function () {
                                                alert('Success: Item deleted');
                                            }
                                    );
                            }

                            // Function to copy a node
                              scope[treeId].copy = function(cnode) {
                                        scope.copiednode = cnode
                                        console.log("Path that is copied: " + scope.copiednode);
                                        // tempNode = cnode;
                                        //  console.log(tempNode);
                            }

                            // function to POST data to server to paste item
                              scope[treeId].paste = function(path) {
                                        console.log("Node to be pasted: " + scope.copiednode);
                                        $http({method: 'POST', url: 'http://localhost:8080' + path + 'paste', data:{'Path': scope.copiednode}}).success(
                                        // $http({method: 'POST', url: 'http://localhost:8080/', data: {ID: itemId, Parent:parentid}}).success(
                                            function () {
                                                alert('Success: Node pasted');
                                            }
                                    );
                            }

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

                                //set currentNode
                                scope[treeId].currentNode = selectedNode;

                                // get path from the node
                                // and go to that path with http
                                var path = scope[treeId].currentNode.Path;
                                $http.get('http://127.0.0.1:8080'+path).success
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
                    }
                }
            };
    }])
    .directive('modalDialog', function() {
          return {
            restrict: 'E',
            scope: {
              show: '='
            },
            replace: true, // Replace with the template below
            transclude: true, // we want to insert custom content inside the directive
            link: function(scope, element, attrs) {
              scope.dialogStyle = {};
              if (attrs.width)
                scope.dialogStyle.width = attrs.width;
              if (attrs.height)
                scope.dialogStyle.height = attrs.height;
              scope.hideModal = function() {
                scope.show = false;
              };
            },
            template: "<div class='ng-modal' ng-show='show'>"+
                                "<div class='ng-modal-overlay' ng-click='hideModal()'></div>"+
                                "<div class='ng-modal-dialog' ng-style='dialogStyle'>"+
                                    "<div class='ng-modal-close' ng-click='hideModal()'>X</div>"+
                                    "<div class='ng-modal-dialog-content' ng-transclude></div>"+
                                "</div>"+
                            "</div>"
          };
    });
})( angular );
