var hmShipServices = angular.module('hmShipServices',[]);

hmShipServices.factory('auctionDataService', [ '$http', '$q',function( $http, $q ){

        return {

            getAutionList: function( ) {
                //var deferred = $q.defer();
                var url = 'api/auctions/';
                return $http({ 
                    method: 'GET', 
                    url: url
                })
                //return deferred.promise;
            }
        };             
}]);


//THIS SERVICE REQUIRED GOOGLE MAPS INITIALIZATION
hmShipServices.factory('googleMapsApiService', [ '$http', '$q',function( $http, $q ){

        return {

            getAutionList: function( ) {
                //var deferred = $q.defer();
                var url = 'api/auctions/';
                return $http({ 
                    method: 'GET', 
                    url: url
                })
                //return deferred.promise;
            }
        };             
}]);



hmShipServices.factory('socialAppService', function($q, $http, $window) {

  //THIS SERVICE REQUIRES THAT THERE BE A FB OBJECT GENERATED AS PER Facebook SDK INSTRUCTIONS

    return {

        getFbToken : function(){
          var deferred = $q.defer();
          FB.login(function(FbResponse){

            if(FbResponse.status == 'connected'){
              var FbData = {
                  'access_token': FbResponse.authResponse.accessToken
              }

              $http.post( 'rest-auth/facebook/', FbData )
                .success(function(DRFResponse){
                  //APP TOKEN AQUIRED
                  $window.sessionStorage.setItem( 'token', DRFResponse.key );
                  deferred.resolve('Success');
                })
                .error(function(DRFError){//deferred.reject(errors);})
                  deferred.reject(DRFError);
                })
            }

          }, {
    scope: 'email', 
    return_scopes: true
});
          return deferred.promise;
        },

        getGoogleToken: function() {
            var deferred = $q.defer();
            GoogleAuth  = gapi.auth2.getAuthInstance();
            GoogleAuth.signIn()
            .then(function( googleResponse){

                //$window.sessionStorage.setItem('profilePicture', googleResponse.Zi)
                var googleData = {
                    'access_token': googleResponse.Zi.access_token
                }

                $http.post( 'rest-auth/google/', googleData )
                .success(function(DRFResponse){

                  //APP TOKEN AQUIRED
                  $window.sessionStorage.setItem( 'token', DRFResponse.key );

                  deferred.resolve('Success');
                })
                .error(function(DRFError){//deferred.reject(errors);})
                  deferred.reject(DRFError);
                })
              
            })
            // .then(function(googleErrorResponse){
            //   deferred.reject(googleErrorResponse);
            // })
    
            return deferred.promise;
        }
    }
}); 


 hmShipServices.factory('arrayServices', function () {

      return {

        arrayFromObjArray: function(arrayOfObjects, key) {       

          var res = [];
          for (var i in arrayOfObjects){
            res.push(arrayOfObjects[i][key])

          }
          return res;


         },
        findObjectInArray: function(arrayOfObjects, key, value) { 

          for (var i in arrayOfObjects){
            if(arrayOfObjects[i][key] == value){
              return arrayOfObjects[i];
            }
          
          }
          return {};


         },
         shuffleArray:function(array){
          var m = array.length, t, i;

          // While there remain elements to shuffle
          while (m) {
            // Pick a remaining element…
            i = Math.floor(Math.random() * m--);

            // And swap it with the current element.
            t = array[m];
            array[m] = array[i];
            array[i] = t;
          }
          return array;
         }
      }
});


hmShipServices.factory('yearListService', function ($window, $q) {

      return {

        request: function() {
          var user_string = $window.sessionStorage.getItem('userDataString');
          var yearList =[];
          if (user_string){
            var year_joined = new Date(JSON.parse(user_string).date_joined).getFullYear();
            var this_year = new Date().getFullYear();

            do {
                yearList.push(year_joined)
                year_joined++;
            }
            while ( year_joined<= this_year);
              return yearList;
          }
          return yearList ;

        }
      }
});

hmShipServices.factory('tokenAuthInterceptor', function ($window, $q, $location) {
    return {
        request: function(config) {

            config.headers = config.headers || {};
            if ($window.sessionStorage.getItem('token')) {
              // may also use localStorage
                config.headers.Authorization = 'Token ' + $window.sessionStorage.getItem('token');
            }
            return config || $q.when(config);
        },
        response: function(response) {
            if (response.status === 401) {
                //  Redirect user to login page / signup Page.
            }
            return response || $q.when(response);
        }
    };
});



hmShipServices.factory('userSessionServices', ['$http', '$window', '$location', '$q', 
  function( $http, $window, $location, $q ){
    var errors =  {};
    var _identity = undefined, _authenticated = false;
    return{
        logIn : function( credentials ){
            var deferred = $q.defer();
            var url = 'rest-auth/login/';
            $http.post(url, credentials).success(function(token){
              
              if( token!= null ){
                deferred.resolve(token.key);
                $window.sessionStorage.setItem('shoppingCart', '[]')
                $window.sessionStorage.setItem( 'token', token.key );

              }else{
                deferred.reject( 'email/password error' );
              }

            })
            .error( function( error ){
              if( error != null ){
             
                for(var field in error){
                  if(field === 'non_field_errors'){
                    errors[field] = error[field].join(', ')
                  }
                }
      
                  deferred.reject( errors );
                  //deferred.reject('error.non_field_errors[0]');
                //     //errors[field] = error[field].join(', ')
                //   }
                // }
                
              }    

              //deferred.reject(errors);
            })
            return deferred.promise;
            //return(token)? token : false;
        },
        logOut : function(){
            var url = '/rest-auth/logout/'
            $http({
              method: 'POST',
              url: url
            }).then(function (response) {
              if (response.status == 200){
                $window.sessionStorage.clear();
                $location.path('/');         
              }


                // this callback will be called asynchronously
                // when the response is available
              }, function errorCallback(response) {
                console.log(JSON.stringify(response))
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              }); 
        },
        isAuthenticated : function(){
          var token = sessionStorage.getItem('token');
          return(token)? true : false;
        },
        updateSessionStorage : function( newUserDataObj ){
          sessionStorage.setItem('userDataString', JSON.stringify(newUserDataObj));
          return 'success';
          // var token = sessionStorage.getItem('token');
          // return(token)? true : false;
        },
        // getSessionStorage : function( ){
        //   var userDataString = sessionStorage.getItem( 'userDataString')
        //   if( userDataString ){
        //     return JSON.parse( userDataString );
        //   }
        //   return userDataString;
        // },
        userProfile : function()
        {
          var deferred = $q.defer();
          var userDataString = sessionStorage.getItem( 'userDataString');
          if( userDataString ){
            deferred.resolve(JSON.parse( userDataString));
            //return JSON.parse( userDataString );
          }else{
            //var deferred = $q.defer();
            //var token = {};
            //var token = sessionStorage.getItem('token');
            //console.log($location.protocol() + "://" + $location.host() + ":" + $location.port());
            var url = $location.protocol() + "://" + $location.host() + ":" + $location.port() + '/api/users/';
            //var url = 'api/users/'

            $http({
              method: 'GET',
              url: url
            }).then(function successCallback( response ) {
                // $window.sessionStorage.setItem('userDataString', JSON.stringify(response.data[0]));
                // var result = {};
                // result.status = 200;
                deferred.resolve( response.data[0] );
                // this callback will be called asynchronously
                // when the response is available
              }, function errorCallback(error) {
                deferred.resolve(error);
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });

            return deferred.promise;
          }
        }
      }

}]);


hmShipServices.factory('reportService', function ($uibModal, $location, $http) {
    return {
        getReport: function(picObj) {

    switch(picObj.object_type) {

        case 'Inspections':
            if(picObj.sample ==true){
              //THIS CODE REQUIRED
                $location.path('sample_inspection_carousel_detail').search({param:picObj.unique_id, type:'sample'})
              //var url = 'api/sample_carousel/' + picObj.unique_id+'/';
            }else{
              $location.path('inspection_carousel_detail').search({param:picObj.obj_id})
            } 
          
            break;

        case 'auction':
        window.location.assign(picObj.url)
            break;

        case 'Logistics':

            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                animation: true,
                templateUrl: '/static/templates/userapp/partials/carouselLogisticsDetailModal.html',
                controller: 'carouselLogisticsDetailModalController',
                size: 'lg',
                resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
                  pdf: function($http){
                    if(picObj.sample ==true){
                      var url = 'api/sample_carousel/' + picObj.unique_id+'/';
                    }else{
                      var url = 'api/logistics_carousel/' + picObj.obj_id+'/';
                    } 
                    
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                  }
                }
            });
        $location.path('logisticsample');
            break;

        case 'Maintenance':
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                animation: true,
                templateUrl: '/static/templates/userapp/partials/carouselLogisticsDetailModal.html',
                controller: 'carouselLogisticsDetailModalController',
                size: 'lg',
                resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
                  pdf: function($http){
                    if(picObj.sample ==true){
                      var url = 'api/sample_carousel/' + picObj.unique_id+'/';
                    }else{
                      var url = 'api/logistics_carousel/' + picObj.obj_id+'/';
                    } 
              return $http({ 
                  method: 'GET', 
                  url: url
              }).then(function(response){
                  return response.data;
              })
                  }
                }
            });
            break;            
        case 'Facebook':
        window.location.replace(picObj.url);
            break;
        case 'Twitter':
        window.location.replace(picObj.url);
            break;
        case 'Instagram':
        window.location.replace(picObj.url);
            break;
        case 'Social Media':
        window.location.replace(picObj.url);
            break;
        default:
          break;
    } 
        }
    };
});

