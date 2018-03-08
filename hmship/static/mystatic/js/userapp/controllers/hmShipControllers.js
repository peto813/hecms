var hmShipControllers = angular.module('hmShipControllers',['hmShipModalControllers']);
 

	hmShipControllers.controller('TwitterRedirectController', ['$scope',
		function( $scope ){

	}])

//								REGISTRATION CONTROLLER
hmShipControllers.controller('joinController', [
	'$scope',
	'$http',
	'$uibModal', 
	'userSessionServices',
	'$window',
	'$rootScope',
	function( $scope, $http, $uibModal, userSessionServices, $window, $rootScope ){


		$scope.errors = {};

		$scope.resetServerValidation = function(){
			$scope.joinForm.email.$setValidity('serverValidation', true );
			$scope.showServerError= false;
		}

		$scope.joinPost = function(){
			if($scope.joinForm.$valid){
		        var url = 'rest-auth/registration/';
		        var data = {
		            //"username": $scope.email,
		            "email": $scope.email,
		            "password1": $scope.password1,
		            "password2": $scope.password2
		        }

		        // postRequest.ajaxPost( url ,data ).success( function( response ){
		        //     $scope.openRegistrationThanksModal('md')
		        // })
		        $http.post(url, data)
				.success( function( response, status ){
					if (status == 201){
						alert('Thank you for registering with Hecms! Please check your inbox and verify your email.');
						$scope.email = '';
						$scope.password1='';
						$scope.password2='';
						$scope.acceptTerms = false;
						$scope.joinForm.$setPristine();
						$scope.joinForm.$setUntouched();
						// $window.sessionStorage.setItem('token', response.key);
				  //   	userSessionServices.userProfile().then(function( userInfo ){
				  //   		$window.sessionStorage.setItem('userDataString', JSON.stringify(userInfo.data));
				  //   		//$rootScope.userdata = JSON.parse($window.sessionStorage.getItem('userDataString'));
				  //   		//$rootScope.userName = String( userInfo.data.first_name + ' ' +userInfo.data.last_name )|| userInfo.data.email;
				  //   		// if(!(userInfo.data.first_name && userInfo.data.last_name)){
				  //   		// 	$rootScope.userName = userInfo.data.email;
				  //   		// }
				  //   		//$window.sessionStorage.setItem('userName', $rootScope.userName)
				  //   		//$location.path('/home');

				  //   		//REDIRECT MODAL
				  //   		$scope.openRegistrationThanksModal('md');
				  //   	});					
					}

		        	
		        })
				.error(function( response ){
	
					if(response){
						for(var field in response){

							if(field != 'username'){
								$scope.joinForm[field].$setValidity('serverValidation', false );
								$scope.errors[field] = response[field].join(', ')
								$scope.showServerError= true;

							}
						}
						
					}
				})		
			}

		}



		$scope.openRegistrationThanksModal = function(size){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: 'static/templates/userapp/partials/registrationThanks.html',
	            controller: 'regThanksModalController',
	            size: 'md'
	            // resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
	            //   minDate: function(){
	            //     return $scope.minDate;
	            //   },
	            //   maxDate: function(){
	            //     return $scope.maxDate;
	            //   },
	            //    fechaEgreso: function(){
	            //     return $scope.fechaEgreso;
	            //   }    
	            // }
	        });
		}

	


}])

//									MODAL CONTROLLER





//								HMSHIP LOGIN CONTROLLERS
hmShipControllers.controller('signInController', [
	'$scope',
 	'$uibModal',
 	'$window',
 	//'ezfb', 
 	'$location',
  	'userSessionServices',
  	'$rootScope',
  	'socialAppService',
  	'$http',
  	'$stateParams',
	function( 
		$scope, 
		$uibModal,
		$window,
		//ezfb, 
		$location, 
		userSessionServices,
		$rootScope ,
		socialAppService,
		$http,
		$stateParams
	){

    //var self = this; //to be able to reference to it in a callback, you could use $scope instead
    // gapi.load('auth2', function() {//load in the auth2 api's, without it gapi.auth2 will be undefined
    //     gapi.auth2.init(
    //             {
    //                 client_id: '112766511222-dbe171oatf6lei1b7eff3a2ehia55i30.apps.googleusercontent.com'
    //             }
    //     );
    // });

$scope.twitterSignIn = function () {
	$http.get('/api/twitteroauth/').success(function(response){
		//var ref = window.open(response, "Twitter Login", "menubar=1,resizable=1,width=350,height=250");
		window.location.href = response;
	})
}

$scope.googleSignIn = function () {
	socialAppService.getGoogleToken().then(function(response) {
		if (response == 'Success'){
	    	userSessionServices.userProfile().then(function( userInfo ){
	    		sessionStorage.setItem('userDataString', JSON.stringify(userInfo));
	    		//$rootScope.userdata = JSON.parse($window.sessionStorage.getItem('userDataString'));
	    		//$rootScope.userName = String( userInfo.data.first_name + ' ' +userInfo.data.last_name )|| userInfo.data.email;
	    		//if(!(userInfo.data.first_name && userInfo.data.last_name)){
	    		//	$rootScope.userName = userInfo.data.email;
	    		//}
	    		//$window.sessionStorage.setItem('userName', $rootScope.userName)
	    		$location.path('home');
	    	});		
		}

	})
}




$scope.loginFB = function() {
	socialAppService.getFbToken().then(function(response) {
		if (response == 'Success'){
	    	userSessionServices.userProfile().then(function( response ){
	    		sessionStorage.setItem('userDataString', JSON.stringify(response));
	    		$location.path('home');
	    		
	    	})
		}

	},
	function(data, status) {
		alert(data);

	})

};


		$scope.loginPost = function(){

			if($scope.loginForm.$valid){

		  //       var url = 'rest-auth/login/';
		        var credentials = {
		            //"username": $scope.email,
		            "email": $scope.email,
		            "password": $scope.password

		        }
		        userSessionServices.logIn( credentials )

			        .then(function( token ){
			        	userSessionServices.userProfile().then(function( response ){
			        		sessionStorage.setItem( 'userDataString', JSON.stringify( response ) );
			        		$location.path('/home');
			        		// if(response.status == 200){
			        		// 	$location.path('/home');
			        		// }
			        		
			        	});
			        	

			        }).catch(function(errors){

			        	$scope.errors = errors
			        })


		  //       $scope.errors = {};
		  //       postRequest.ajaxPost( url ,data ).success( function( response ){
		  //       	if(response.key){
		  //       		//get user information
		  //       		$rootScope.userProfile = userSessionServices.userProfile();
			 //        	$window.sessionStorage.setItem( 'token', response.key);
			 //        	$location.path('/home');	  		
		  //       	}

		  //       })
				// .error(function( response ){
				// 	if(response){
				// 		for(var field in response){

				// 			if(field === 'non_field_errors'){
				// 				$scope.errors[field] = response[field].join(', ')
				// 			}
				// 		}
						
				// 	}
				// })	

			}

		}

}])

hmShipControllers.controller('ErrormessageController', ['$scope',
	function( $scope ){
		$scope.messages = [
			{
				'expression' : 'required',
				'description' : 'This field is required'
			},
			{
				'expression' : 'email',
				'description' : 'Invalid email address'
			},
			{
				'expression' : 'number',
				'description' : 'This field only accepts numbers'
			},	
			{
				'expression' : 'passwordMatch',
				'description' : 'Passwords do not match'
			},
			{
				'expression' : 'fieldMatch',
				'description' : 'Fields do not match'
			}
		]
}])


//								HMSHIP FORGOT PASSWORD CONTROLLERS
hmShipControllers.controller('forgotPwdController', ['$scope', '$http',
	function( $scope, $http ){
		$scope.formData = {};
		$scope.recoverPwd = function(){
			if($scope.recoverPwdForm.$valid){
				var url = 'rest-auth/password/reset/';
				$http.post( url, $scope.formData ).success( function( response, status ){
					if(status == 200){
						$scope.formData = {};
						$scope.recoverPwdForm.$setUntouched();
						$scope.recoverPwdForm.$setPristine();
						alert(response.detail);
					}

				})
				.error(function(errors){
					console.log(errors)
					alert( String(errors.email) );
				})				
			}

		}
}])



// hmShipControllers.controller('changePwdModalController', function( $scope, $uibModalInstance, $location, $http, userSessionServices ) {

// 	$scope.showSuccessMessage = false;
// 	$scope.errors = {};
// 	$scope.changePwdPut = function(){
// 		if($scope.changePwdForm.$valid){
// 			data = {
// 				'old_password' : $scope.oldPwd,
// 				'new_password' : $scope.newPwd1,
// 				'new_password_confirm' : $scope.newPwd2
// 			}
// 			$http.put('api/changepassword/', data)
// 			.success(function( successResponse ){
// 				if(successResponse == 'Success'){
// 					$scope.showSuccessMessage = true;
// 				}
// 			})
// 			.error(function	( errorResponse ){

// 				$scope.errors = errorResponse;
// 			})
// 		}
// 	}

// 	$scope.cancel = function () {
// 		$uibModalInstance.dismiss('cancel');
// 	};

// 	// $scope.close = function(){
// 	// 		$uibModalInstance.close(function(){
// 	// 			userSessionServices.logout();
// 	// 		}
// 	// 	)
// 	// }
// });




hmShipControllers.controller('homePageController', ['$scope','auctions',
	function( $scope, auctions ){
		$scope.auctions = auctions
		//$scope.pageClass = 'page-home'
}])


hmShipControllers.controller('contactUsController', ['$scope', '$http',
	function( $scope, $http ){
		$scope.formData = {};
		$scope.sendEmail = function(){
			if ($scope.contactUsForm.$valid){
				$http.post('api/contactus/', $scope.formData).success( function( response, status ){
					if(status == 200){
						$scope.formData = {};
						$scope.contactUsForm.$setUntouched();
						$scope.contactUsForm.$setPristine();
						alert('Thank you for your interest in Hecms, we will review your inquiry and get back to you as soon as possible!');
					}
				})
			}
		}
		//$scope.pageClass = 'page-home'
}])

hmShipControllers.controller('profileController', ['$scope', '$uibModal', '$http', '$window', '$rootScope', 'Upload', '$timeout', 'sessionData',
	function( $scope, $uibModal, $http, $window, $rootScope, Upload, $timeout, sessionData ){

		$scope.phoneNumber = /^[0-9]{9,12}$/;
		$scope.userdata = {};

		if(sessionData.userprofile){
			$scope.userdata.company_name = sessionData.userprofile.company_name;
			$scope.mobile_number = sessionData.userprofile.mobile_number;
			$scope.office_number = sessionData.userprofile.office_number;
			$scope.profile_picture = sessionData.userprofile.profile_picture || 'static/img/pictureplaceholder.jpg';
		}

		//$scope.userdata.company_name = sessionData.userprofile.company_name;
		$scope.userdata.first_name = sessionData.first_name;
		$scope.userdata.last_name = sessionData.last_name;
		//$scope.mobile_number = sessionData.userprofile.mobile_number;
		//$scope.office_number = sessionData.userprofile.office_number;

		$scope.updateContactInfo = function(){
			var data = {};
			data.mobile_number = $scope.mobile_number;
			data.office_number = $scope.office_number;
			var url = 'api/userprofile/' + String(sessionData.userprofile.id)+'/';
			$http.patch(url, data).success(function(userProfile, status){
				if (status == 200){
					var sessionData = JSON.parse(sessionStorage.getItem('userDataString'));
					sessionData.userprofile.mobile_number = userProfile.mobile_number;
					sessionData.userprofile.office_number = userProfile.office_number;
					sessionStorage.setItem('userDataString', JSON.stringify(sessionData));
					alert('Contact Info Updated');
				}
			}).error(function(error, status){
				console.log(error)
			})
		}


		$scope.removepic = function(){

			confirmation = confirm('Are you sure you wish to delete your profile picture?')
			if (confirmation && sessionData.userprofile){
				var data = {};
				data.profile_picture = '';
				$http.patch('api/userprofile/' + String(sessionData.userprofile.id) + '/', data)

					.then(function(response){
					   if (response.status == 200) {
					   		sessionData.userprofile.profile_picture = 'static/img/pictureplaceholder.jpg';
					   		$scope.profile_picture = 'static/img/pictureplaceholder.jpg';
					   		sessionStorage.setItem('userDataString', JSON.stringify(sessionData));				        //$scope.files.splice(idx, 1);
					   	}
					});
			}
			return false;


		}

		$scope.uploadFiles = function(file, errFiles) {

		        $scope.f = file;
		        
		        $scope.errFile = errFiles && errFiles[0];
		        if (file) {
		            file.upload = Upload.upload({
		                url: 'api/userprofile/' + String(sessionData.userprofile.id)+'/',
		                //url: 'api/test/',
		                data: {profile_picture : file },
		                method: 'PATCH',
		                arrayKey: ''
		            });

		            file.upload.then(function (response) {

		                $timeout(function () {
		                    file.result = response.data;
		                    if( response.status == 200 ){
		                    	$scope.profile_picture = response.data.profile_picture;
		                    	sessionData.userprofile.profile_picture = $scope.profile_picture ;
		                    	//userSessionServices.updateSessionStorage(sessionData);
		                    	sessionStorage.setItem('userDataString', JSON.stringify(sessionData ));
		                    }
		                });
		            }, function (error) {
		                if (error.status > 0)
		                    $scope.errorMsg = error.status + ': ' + error.data;
		            }, function (evt) {
		                file.progress = Math.min(100, parseInt(100.0 * 
		                                         evt.loaded / evt.total));
		            });
		        }   
		    }



    // $scope.submit = function() {
    //   if ($scope.form.file.$valid && $scope.file) {
    //     $scope.upload($scope.file);
    //   }
    // };
///////////////////////////


		$scope.postNameChange = function(){
			if($scope.nicknameForm.$valid){
				nameObject = {
					'first_name': $scope.userdata.first_name,
					'last_name': $scope.userdata.last_name,
					'userprofile':{
						'company_name': $scope.userdata.company_name || undefined
					}
					
				}
				userdata = JSON.parse(sessionStorage.getItem('userDataString'))
				$http.patch('api/users/' + String(userdata.id)+'/' , nameObject).success(function( newUserObject ){
					//$window.sessionStorage.setItem('firstName', newUserObject.first_name );
					//$window.sessionStorage.setItem('lastName', newUserObject.last_name );
					// $rootScope.userdata.company_name = newUserObject.company_name;
					// $rootScope.userdata.first_name = newUserObject.first_name;
					// $rootScope.userdata.last_name = newUserObject.last_name;
					sessionStorage.setItem('userDataString', JSON.stringify(newUserObject))
					//$scope.userName()
					//$scope.$disgest();
					// $rootScope.userName = String( newUserObject.first_name + ' ' +newUserObject.last_name) || newUserObject.email;
					alert('Data Succesfully Modified')
				}).error( function( error ){
					console.log( JSON.stringify( error ) )
				})
			}
		}

		$scope.fileUpload = function () {
			document.getElementById('imageUploadLabel').click();
		}


		$scope.imgSrc = function(){
			if($scope.userLogo){
				var path = ''
			}else{
				var path = 'static/img/pictureplaceholder.jpg'
			}
			return path;
		}


		$scope.changePwdModal = function(size){
	        var modalInstance = $uibModal.open({
	            ariaLabelledBy: 'modal-title',
	            ariaDescribedBy: 'modal-body',
	            animation: $scope.animationsEnabled,
	            templateUrl: '/static/templates/userapp/partials/changePassword.html',
	            controller: 'changePwdModalController',
	            size: 'md'
	            // resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
	            //   minDate: function(){
	            //     return $scope.minDate;
	            //   },
	            //   maxDate: function(){
	            //     return $scope.maxDate;
	            //   },
	            //    fechaEgreso: function(){
	            //     return $scope.fechaEgreso;
	            //   }    
	            // }
	        });

		    // modalInstance.result.then(function (changePwdResult) {
		    // 	if(changePwdResult == 'Success'){
		    // 		$scope.showSuccessMessage = true;
		    // 	}
		    // })
		    // , function () {
		    //   $log.info('Modal dismissed at: ' + new Date());
		    // });
		}



}])

hmShipControllers.controller('navBarController', ['$scope', '$http', 'userSessionServices', '$rootScope', '$window',
	function( $scope, $http, userSessionServices, $rootScope, $window){

		$scope.userdata = {}

		$scope.navbar_manipulated = false;
		$scope.toggleCollapse = function(){
			if(innerWidth<=768 && $scope.navbar_manipulated == false){
				$scope.navCollapsed = true;
				$scope.$apply()
			}
		}

		$scope.userName = function(){
			userdata = JSON.parse(sessionStorage.getItem('userDataString'))
			if( userdata ){
				if (userdata.last_name || userdata.first_name){
					var result = (userdata.first_name + ' '  + userdata.last_name);
					return result;
				}else if( userdata.email){
					return userdata.email;
				}else{
					return 'No name/email';			
				}
			}
		}

		if(document.documentElement.clientWidth <=768){
			$scope.navCollapsed = true;
		}
		//$rootScope.userName= $window.sessionStorage.getItem('userName')



		//$scope.userAuthenticated = userSessionServices.isAuthenticated()
		// $scope.userAuthenticated =function(){
		// 	return (userSessionServices.isAuthenticated());
		// } 

		$scope.navbarToggler = function(){
			if ($scope.navCollapsed == false){			
				$scope.navCollapsed = true;
			}
		}
		
		// $scope.brandUrl= function(){
		// 	if (userSessionServices.isAuthenticated()){
		// 		var url = "#/home";
		// 		return url;
		// 	}
		// 	var url = "#/";
		// 	return url;
		// }
		
		$scope.logout = function(){
			userSessionServices.logOut()
		}
	}
])




hmShipControllers.controller('logisticsController', 
	['$scope',
	'$http', 
	'userProducts',
	'$location',
	'$rootScope',
	function( 
		$scope,
		$http,
		userProducts,
		$location,
		$rootScope
		){

	$scope.pageClass = 'logistics';
	// SCOPE INITIAL DEFINITIONS
	$scope.selectedPurchases = [];
	$scope.tableLength = 0;
	$scope.userProducts  = userProducts;
	
	$scope.auctionItems = function(){
		var product_list= [];
		// angular.forEach($scope.userProducts, function(value, key){
		// });

		for (var i in $scope.userProducts){
			if ($scope.userProducts[i].auction.id == $scope.auctionSite){
				product_list.push($scope.userProducts[i]);
			}
		}
		return product_list;
	}


	$scope.googleOtherOriginData = {};
	$scope.googleDestinationData = {};
	$scope.originSelect = 'auction';
	$scope.locationData = {};
	$scope.otherOrigin = '';
	$scope.otherOriginReset = function(){
		if($scope.originSelect == 'auction'){
			$scope.otherOrigin = '';
		}
	}

	$scope.auctionList = function(){
		var auctions_new_list = [];
		for (var i in $scope.userProducts){
			var j = 0;
			var value_found = false;
			for ( j in auctions_new_list){
				if ($scope.userProducts[i].auction.id == auctions_new_list[j].id){
					value_found =true;
				}

			}
			if (value_found  === false){
				auctions_new_list.push($scope.userProducts[i].auction);
			}
		}
		return auctions_new_list;
	}

	$scope.products_list = function(){
		var products_list = []
		var i = 0;
		for (var i in $scope.userProducts){
			if($scope.userProducts[i].auction == $scope.auctionSite){
				products_list.push($scope.userProducts[i]);
			}
		}
		return products_list;
	}


	//SCOPE FUNCTIONS
	$scope.requestLogisticsService = function(){
		if ($scope.logisticsForm.$valid){

			var formData = {};
			formData.products = $scope.selectedPurchases;
			//CLEAN PRODUCTS LIST
			var clean_list = [];
			for (var i in formData.products){
				for (var property in formData.products[i]) {
					if(property=='id'){
						clean_list.push(formData.products[i][property])
					}
				}
			}
			formData.products = clean_list;
			formData.originSelect = $scope.originSelect;
			formData.destination = $scope.destination;
			formData.description = $scope.description;

			formData.destination_lon = $scope.googleDestinationData.longitude
			formData.destination_lat = $scope.googleDestinationData.latitude

			formData.origin_lat = $scope.googleOtherOriginData.latitude
			formData.origin_lon = $scope.googleOtherOriginData.longitude

			if ( $scope.originSelect == 'other' ){
				formData.otherOrigin = $scope.otherOrigin;
				//formData.otherOriginLat = ;
			}

			$http.post( 'api/logistics/', formData ).success(function(response, status){


				if (status === 200){
					// $scope.locationData = {};
					// $scope.otherOrigin  ='';
					// $scope.originSelect = 'auction';
					// $scope.selectedPurchases = [];
					// $scope.destination = '';
					// $scope.description = '';
					// $scope.auctionItem = '';
					// $scope.auctionSite = '';
					// $scope.googleOtherOriginData = {};
					// $scope.googleDestinationData = {};
					// $scope.userProducts = response;
					// $scope.logisticsForm.$setUntouched();
					// $scope.logisticsForm.$setPristine();
					$rootScope.requestedserviceType = 'Logistics';
					$location.path('serviceRequestThanks');
				}
				//alert('Your Logistics request has been submitted, one of our analysts will get back to you very soon!')
			})
			// .error(function(errors){
			// })
		}
	}



	// $scope.geolocate = function(){
 //        if (navigator.geolocation) {
 //          navigator.geolocation.getCurrentPosition(function(position) {
 //            var geolocation = {
 //              lat: position.coords.latitude,
 //              lng: position.coords.longitude
 //            };
 //            var circle = new google.maps.Circle({
 //              center: geolocation,
 //              radius: position.coords.accuracy
 //            });
 //            autocomplete.setBounds(circle.getBounds());
 //          });
 //        }
	// }


/////////////////////////////////////////////////////////////////////
	$scope.resetSelect = function(){
		$scope.auctionItem = '';
	}
	// $scope.tableFilled = function(tableLength){
	// 	return tableLength;
	// }

	$scope.itemSelected = function( item ){
		var found = false; 
		for ( var i in $scope.selectedPurchases){
			if ($scope.selectedPurchases[i].id == item.id){
				found = true;
			}
		}
		return found;
	}
	
	$scope.deleteFromList = function( id ){
		for (var i in $scope.selectedPurchases){
			if( $scope.selectedPurchases[i].id  == id){

				$scope.selectedPurchases.splice(i, 1);
				$scope.tableLength = $scope.selectedPurchases.length;
			}
		}
		//$scope.selectedPurchases.pop()
	}


	$scope.addPurchase = function(){
		var itemInList = false;
		var i = 0;
		var auctionItem = JSON.parse( $scope.logisticsForm.auctionItem.$viewValue );
		var userProducts = $scope.userProducts;
		var selectedPurchases = $scope.selectedPurchases;

		//need to make sure you cant add items from different auction
		for (var item in selectedPurchases){
			if (selectedPurchases[item].auction.id != auctionItem.auction.id){
				alert( 'Can´t add items from another auction!');
				return false;
			}
		}

		if( auctionItem ){
			if( selectedPurchases.length > 0 ){
				for (var i in selectedPurchases){
					if (selectedPurchases[i].id == auctionItem.id){
						itemInList = true;
					}
				}

				if(itemInList == false){
					$scope.selectedPurchases.push( auctionItem );
					$scope.tableLength = $scope.selectedPurchases.length;
				}
			}else{
				$scope.selectedPurchases.push( JSON.parse($scope.logisticsForm.auctionItem.$viewValue) );
				$scope.tableLength = $scope.selectedPurchases.length;
			}
		}
	$scope.auctionItem = '';
	
	}


}])

hmShipControllers.controller('orderBookController', ['$scope', 'OrderBook',	'$uibModal', '$window', '$location', 'shoppingCart', '$http', 'yearListService','reportService',function( $scope, OrderBook, $uibModal, $window, $location, shoppingCart, $http, yearListService, reportService ){
	
	$scope.transclusion = {};
	$scope.transclusion.dateRange = 'last30';
	$scope.OrderBook = OrderBook;
	$scope.yearRange = yearListService.request()
	$scope.shoppingCart = shoppingCart;
	$scope.selectAllChx = false;


	$scope.queryDate = function(dateRange){

		switch(dateRange) {

		    case 'last30':
		    	var now_date = new Date()
		    	var timestamp_lte = new Date();
		        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
		        break;

		    case 'months-6':
		    	var now_date = new Date()
		    	var timestamp_lte = new Date();
		        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
		        break;

		    default:
		    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
		        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
		} 


		var url = 'api/services/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
		$http.get(url).success(function(response ){

			if(response.length == 0){
				$scope.results = '0 Results Found;'
			}else{

				$scope.OrderBook = response;
				$scope.searchParam = '';
				
			}
		})	
	
	}


	$scope.refreshList = function(){
		$scope.OrderBook = OrderBook;
		$scope.results_count = 0;
		$scope.transclusion.dateRange = 'last30';
	}

	$scope.searchBackend = function(){

		var url = 'api/services?search_param=' + $scope.searchParam;

		$http.get(url).success(function(response ){

			if(response.length == 0){
				$scope.results = '0 Results Found;'
			}else{
				$scope.searchParam = '';
				$scope.OrderBook = response;
			}
		})	
	}


	$scope.itemInCart = function (serviceId){
		var id_list = [];
		for ( var i in $scope.shoppingCart ){
			id_list.push( $scope.shoppingCart[i].id );
		}

		if (id_list.indexOf(serviceId) == -1){
			return false;
		}
		return true;

	}


	$scope.makePayment = function(){

		var paymentList = [];
		var shopping_cart = JSON.parse(sessionStorage.getItem('shoppingCart'))||[];
		//ADD CHECKED ITEMS TO CART

		for (var i in $scope.OrderBook){
			if ($scope.OrderBook[i].checked && $scope.OrderBook[i].quote_approved){
				$scope.OrderBook[i].status = 'In Shopping Cart'
				//$scope.$apply();
				shopping_cart.push($scope.OrderBook[i]);
			}
		}
		if(shopping_cart===null || shopping_cart.length == 0 || shopping_cart===undefined){
			alert('You have not selected any items from the list');
			return false;
		}
		//STORE CART IN LOGAL STORAGE

		sessionStorage.setItem('shoppingCart', JSON.stringify(shopping_cart));
		//REDIRECT TO SHOPPING CART
		$location.path('payments1');
	}

	$scope.quotesApproved = function(){
		var quote_approved = false;
		for ( var i in $scope.OrderBook){
			if ($scope.OrderBook[i].quote_approved == true){
				quote_approved = true;
			}
		}
		return quote_approved;
	}

	$scope.selectAllChx = function(){
	
		$scope.selectAll = !$scope.selectAll;
		for (var i in $scope.OrderBook){
			if($scope.OrderBook[i].quote_approved && $scope.OrderBook[i].quote_price && !$scope.OrderBook[i].quote_payed && $scope.itemInCart($scope.OrderBook[i].id)){
				$scope.OrderBook[i].checked = $scope.selectAll;
			}
	
		}

	}

	function viewQuote(service){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/service_quote.html',
            controller: 'quoteController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              service: function(){
                return service;
              }
            }


        });

	    modalInstance.result.then(function (service) {
	    	for (var i in $scope.OrderBook){
	    		if (service.id == $scope.OrderBook[i].id ){
	    			$scope.OrderBook[i]  = service;
	    			break;
	    		}
	    	}
	    	alert('Your quote has been accepted, feel free to choose the services that you wish to pay for from the list.')
	    });
	}

	function showPendingQuoteModal(message){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/pendingQuoteModal.html',
            controller: 'pendingQuoteModalController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              message: function(){
                return message;
              }
            }
        });
	}

	$scope.serviceAction = function( service  ){

		if( service.status == 'Pending Quote' ){
			var message = 'One of our service representatives is tending to your request, we will contact you as soon as we have prepared a quote for this service.'
			showPendingQuoteModal( message );
		}else if( service.status == 'Quote Pending Client Approval' ){
			viewQuote( service );
		}else if( service.status == 'Pending Payment' ){
			var message = 'Please select the items you wish to pay and click the Shopping Car Button';
			showPendingQuoteModal( message );
		}else if( service.status == 'Pending Hecms Approval' ){
			var message = 'You will be notified via email once your payment has been reviewed!';
			showPendingQuoteModal(message);
		}else if( service.status == 'Resolved' ){
			
			var obj = {
				obj_id : service.id,
				object_type : service.service_type
			}
			reportService.getReport(obj)

		}else if( service.status == 'Payed'){
			var message = 'Your payment has been credited, you will be notified of service updates via email'
			showPendingQuoteModal(message);
		}
	}

	$scope.serviceDetail = function( service ){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/serviceDetail.html',
            controller: 'serviceDetailsModalController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              service: function(){
                return service;
              }
            }
        });
	}


	$scope.orderBookTabList = [
		//{ url : 'auctionproducts', name : 'Register Purchases'  },
		{ url : 'editauctionproducts', name : 'Edit Purchases'  },
		{ url : 'orderbook', name : 'Order Book'  },
		//{ url : 'orderhistory', name : 'Order History'  },
		{ url : 'paymenthistory', name : 'Payment History'  }
		//{ url : 'paymenthistory', name : 'Payment History'  }
	]




	// $scope.OrderBookDetails = function(instance){
 //        var modalInstance = $uibModal.open({
 //            ariaLabelledBy: 'modal-title',
 //            ariaDescribedBy: 'modal-body',
 //            animation: $scope.animationsEnabled,
 //            templateUrl: '/static/templates/userapp/partials/orderBookDetails.html',
 //            controller: 'orderBookDetailsController',
 //            size: 'md',
 //            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
 //              order: function(){
 //                return instance;
 //              }
 //              // maxDate: function(){
 //              //   return $scope.maxDate;
 //              // },
 //              //  fechaEgreso: function(){
 //              //   return $scope.fechaEgreso;
 //              // }    
 //            }
 //        });
	// }

	$scope.colList = [ 
		{'key':'id', 'title':'Service ID'}, 
		{'key':'service_type', 'title':'Type'},
		// {'key':'host', 'title':'Auction'}, 
		// {'key':'auction_begin', 'title':'Auction Date'}, 
		{'key':'created', 'title':'Request Date'}, 
		{'key':'status', 'title':'Status'}

	];

	$scope.eraseSelection = function (){
		var del_list = [];
		for (var row in $scope.purchases){
			if ($scope.purchases[row].checked == true && $scope.purchases[row].has_open_process == false){
				del_list.push($scope.purchases[row].id)
			}
		}
		if (del_list.length == 0){
			alert('Please select the items you wish to delete');
			return false;
		}
		var delete_answer =  confirm("Are you sure you wish to delete the selected purchases?");
		var data = {}
		data.del_list  = del_list
		var url = 'api/deleteauctionproducts/';
		if (delete_answer){
			$http.post(url, data).success(function(purchases, status){
				//$scope.purchases = purchases;
				if(status == 200){
					alert('Your auction purchases have been deleted');
				}
			})
			.error(function(errors, status){
				console.log(status);
			})
		}else{
			return false;
		}
		
	}



}])


hmShipControllers.controller('serviceRequestThanksController', ['$scope', '$rootScope',	function( $scope, $rootScope ){
	
}])

hmShipControllers.controller('bankDepositController', ['$scope', '$rootScope', 'bankAccounts', '$uibModal', function( $scope, $rootScope, bankAccounts, $uibModal ){
	
	$scope.bankAccounts = bankAccounts;
	$scope.shoppingCart = JSON.parse(sessionStorage.getItem('shoppingCart'));

	$scope.showBank = function(){
		if ($scope.bank){
			return JSON.parse($scope.bank);	
		}
		return false;
	}

	$scope.total = function(){
		var total = 0;
		for (var i in $scope.shoppingCart){
			total += parseFloat($scope.shoppingCart[i].quote_price);
		}
		return total;
	}

	$scope.registerPayment = function(bank){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/registerPaymentModal.html',
            controller: 'registerPaymentModalController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              bank: function(){
                return JSON.parse(bank);
              },
              total: function(){
              	return $scope.total();
              }
            }
        });
		//$location.path('registerPayment')
	}
}])

hmShipControllers.controller('shoppingCartController', ['$scope', '$rootScope',	'shoppingCart', '$window',function( $scope, $rootScope, shoppingCart, $window ){
	
	$scope.shoppingCart = shoppingCart;
	$scope.pageClass = 'page-shopping-cart';
	$scope.eraseItemFromCart = function( item ){
		var confirmation = confirm('Are you sure you wish to erase this item from the shopping cart?')
		if (confirmation){
			for(var i in $scope.shoppingCart){
				if ($scope.shoppingCart[i].id == item.id ){
					$scope.shoppingCart.splice(i, 1);
				}
			}
			if($scope.shoppingCart.length == 0){
				sessionStorage.setItem('shoppingCart', '[]');
			}else{
				sessionStorage.setItem('shoppingCart', JSON.stringify($scope.shoppingCart));
			}
		}else{
			return false;
		}

	}

	$scope.totalDue = function(){
		var total = 0;
		for (var i in $scope.shoppingCart){
			total += parseFloat($scope.shoppingCart[i].quote_price);
		}
		return total;
	}


	$scope.get_description = function(item){ 

		if ($scope.shoppingCart.length >0 && item){
			if (item.service_type =='Inspections'){
				return item.inspections.description;
			}else if(item.service_type =='Logistics'){
				return item.logistics.description;
			}
			else if(item.service_type =='Maintenance'){
				return item.maintenance.description;
			}
		}else{
			return false;
		}
	}

}])

hmShipControllers.controller('InspcarouselDetailController', ['$scope', '$rootScope', '$location', '$http','$uibModal',function( $scope, $rootScope, $location, $http, $uibModal ){
	
	var url_param = $location.search();
  	$scope.rate = 7;
  	$scope.max = 4;
  	$scope.isReadonly = true;
  	$scope.gallery = []
  	//$scope.htmlTooltip = $sce.trustAsHtml('I\'ve been made <b>bold</b>!');

  	$scope.viewPicture = function(picture){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/inspPicModal.html',
            controller: 'inspPicModalController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              picture: function(){
                return picture;
              }
            }
        });
  	}

  	$scope.htmlTooltip=function(rating){
  		return ['1 Star: Ned', 'peo', 'caca',];
  	}

	 $scope.hoveringOver = function(value) {
	    $scope.overStar = value;
	    $scope.percent = 100 * (value / $scope.max);
	  };


	var url = 'api/inspection_carousel/';

	$http.get(url+url_param.param).success(function(report, status){
		console.log(report)
		if(status ==200){
			var picture_present = false;
			$scope.report= report;
			var gallery = [];
			for (var i in report.rows){
				gallery.push(report.rows[i]);
				if(report.rows[i].item_picture){
					picture_present = true;
				}
			}

			if(picture_present == false){
				$scope.gallery = [{item_picture:'/static/img/imageri/no-image.png'}]
			}else{
				$scope.gallery = gallery;
			}

			
		}

	})


}])

hmShipControllers.controller('auctionCarouselDetailController', ['$scope', '$rootScope', '$location', '$http',function( $scope, $rootScope, $location, $http ){
	
	var url_param = $location.search();
	$scope.auction_details = $location.search();

}])

hmShipControllers.controller('InspcarouselSampleDetailController', ['$scope', '$rootScope', '$location', '$http','$uibModal',function( $scope, $rootScope, $location, $http, $uibModal ){
	
	var url_param = $location.search();
  	$scope.rate = 7;
  	$scope.max = 4;
  	$scope.isReadonly = true;
  	$scope.gallery = []
  	//$scope.htmlTooltip = $sce.trustAsHtml('I\'ve been made <b>bold</b>!');

  	$scope.viewPicture = function(picture){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/inspPicModal.html',
            controller: 'inspPicModalController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              picture: function(){
                return picture;
              }
            }
        });
  	}

  	$scope.htmlTooltip=function(rating){
  		return ['1 Star: Ned', 'peo', 'caca',];
  	}

	 $scope.hoveringOver = function(value) {
	    $scope.overStar = value;
	    $scope.percent = 100 * (value / $scope.max);
	  };


	$http.get('api/inspection_carousel_sample_detail/'+url_param.param).success(function(report, status){

		if(status ==200){
			$scope.sections = report.sections
			var picture_present = false;
			$scope.report= report;
			$scope.rows=report.rows;
			var gallery = [];
			for (var i in report.rows){
				gallery.push(report.rows[i]);
				if(report.rows[i].image){
					picture_present = true;
				}
			}

			if(picture_present == false){
				$scope.gallery = [{image:'/static/img/imageri/no-image.png'}]
			}else{
				$scope.gallery = gallery;
			}

			
		}

	})
	
}])



hmShipControllers.controller('orderHistoryController', ['$scope', '$rootScope',	function( $scope, $rootScope ){

	$scope.minDate = new Date();
	$scope.maxDate = new Date();

	$scope.colList = [ 
		{'key':'lot_number', 'title':'Lot Number'}, 
		{'key':'id', 'title':'Item'}, 
		{'key':'host', 'title':'Auction'}, 
		{'key':'auction_begin', 'title':'Auction Date'}, 
		{'key':'edit', 'title':'Modify'}, 
		// {'key':'id', 'title':'Status'}
	];

	$scope.orderBookTabList = [
		{ url : 'orderbook', name : 'Open Orders'  },
		{ url : 'orderhistory', name : 'Order History'  },
		{ url : 'paymenthistory', name : 'Payment History'  }
	]


}])

hmShipControllers.controller('testController', ['$scope', '$rootScope',	'imageri','$location',function( $scope, $rootScope, imageri, $location ){

	$scope.landing_page_imageri = imageri.landing_page_imageri;

	$scope.openCarouselImg = function(imageId){
		$location.path('carousel_detail').search({param:imageId})
	}

	function getCarousel(images){
		var carousel = [];
		var i = 0;
		var arr1 = [];
		var arr2 = [];
		for (var i in images){
			i>5 ? arr2.push(images[i]) : arr1.push(images[i]) 
			
			i++;
		}

		carousel.push(arr1);
		carousel.push(arr2)
		return carousel;
	}

	$scope.gallery = getCarousel(imageri.carousel_imageri)
	$scope.slides = imageri.carousel_imageri;


	var slides = $scope.slides ;

  	$scope.myInterval = 5000;
  	$scope.noWrapSlides = false;
  	$scope.active = 0;
  	//$scope.slides = imageri.carousel_imageri;
  	var currIndex = 0;

// $scope.getSecondIndex = function(index){
//     if(index-slides.length>=0)
//       return index-slides.length;
//     else
//       return index;
//   }

  $scope.addSlide = function() {
    //var newWidth = 600 + slides.length + 1;
    slides.push({
      //image: '//unsplash.it/' + newWidth + '/300',
      //image:imageri.carousel_imageri[0]['image'],
      image:'https://www.google.co.ve/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwiWufmuwP3TAhXHKiYKHQ7tC70QjRwIBw&url=http%3A%2F%2Fwww.defenseindustrydaily.com%2Ff22-raptor-procurement-events-updated-02908%2F&psig=AFQjCNHuT2VSsYUWM7bUNw-0QnBlSHL1SA&ust=1495336396854601',
      text: ['Nice image','Awesome photograph','That is so cool','I love that'][slides.length % 4],
      id: currIndex++
    });
  };




  $scope.randomize = function() {
    var indexes = generateIndexesArray();
    assignNewIndexesToSlides(indexes);
  };

  for (var i = 0; i < 4; i++) {
    //$scope.addSlide();
  }

  // Randomize logic below

  function assignNewIndexesToSlides(indexes) {
    for (var i = 0, l = slides.length; i < l; i++) {
      slides[i].id = indexes.pop();
    }
  }

  function generateIndexesArray() {
    var indexes = [];
    for (var i = 0; i < currIndex; ++i) {
      indexes[i] = i;
    }
    return shuffle(indexes);
  }

  // http://stackoverflow.com/questions/962802#962890
  function shuffle(array) {
    var tmp, current, top = array.length;

    if (top) {
      while (--top) {
        current = Math.floor(Math.random() * (top + 1));
        tmp = array[current];
        array[current] = array[top];
        array[top] = tmp;
      }
    }

    return array;
  }

}])



hmShipControllers.controller('paymentHistoryController', ['$scope', '$rootScope', 'paymentHistory', '$uibModal', '$http', 'yearListService',function( $scope, $rootScope, paymentHistory, $uibModal, $http, yearListService ){

	$scope.yearRange = yearListService.request()
	$scope.transclusion = {};
	$scope.transclusion.dateRange = 'last30';
	$scope.paymentHistory = paymentHistory;

	$scope.searchBackend = function(){

		var url = 'api/payments?search_param=' + $scope.searchParam
		$http.get(url).success(function(response ){
			if(response.length == 0){
				$scope.results = '0 Results Found;'
			}else{
				$scope.searchParam = '';
				$scope.purchases = response;
			}
		})	
	}


	$scope.queryDate = function(dateRange){

		switch(dateRange) {

		    case 'last30':
		    	var now_date = new Date()
		    	var timestamp_lte = new Date();
		        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
		        break;

		    case 'months-6':
		    	var now_date = new Date()
		    	var timestamp_lte = new Date();
		        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
		        break;

		    default:
		    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
		        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
		} 


		var url = 'api/payments?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
		$http.get(url).success(function(response ){
			
			if(response.length == 0){
				$scope.results = '0 Results Found;'
			}else{
				$scope.purchases = response;
				$scope.searchParam = '';
				
			}
		})	
	
	}

	$scope.refreshList = function(){
		$scope.paymentHistory = paymentHistory;
		$scope.results_count = 0;
		$scope.transclusion.dateRange = 'last30';
	}

	$scope.payment_status = function ( payment ) {
		var payment_status = 'Awaiting Approval';
		if ( payment.payment_approved == false ){
			return 'Payment Rejected';
		}else if( payment.payment_approved == true ){
			return 'Payment Approved';
		}
		return payment_status;
	}
	$scope.colList = [ 
		{'key':'id', 'title':'ID'}, 
		{'key':'amount', 'title':'Amount'}, 
		{'key':'created', 'title':'Created'}, 
		{'key':'payment_type', 'title':'Type'}, 
		//{'key':'edit', 'title':'Modify'}, 
		{'key':'payment_approved', 'title':'Status'}
	];


	$scope.orderBookTabList = [
		{ url : 'editauctionproducts', name : 'Edit Purchases'  },
		{ url : 'orderbook', name : 'Order Book'  },
		{ url : 'paymenthistory', name : 'Payment History'  }
	]

	$scope.paymentDetails = function(row){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/paymentdetailsModal.html',
            controller: 'paymentDetailsController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              row: function(){
                return row;
              }
            }
        });
	}


}])


hmShipControllers.controller('indexController', ['$scope', '$rootScope','gallery','$location','$uibModal','reportService',function( $scope, $rootScope, gallery, $location, $uibModal, reportService ){

	$scope.token = sessionStorage.getItem('token');
	$scope.auctions = gallery.auctions;
	//LANDING PAGE IMAGES
	$scope.gallery = gallery.carousel_gallery
	$scope.imageri = gallery.landing_page_imageri;

	var slides = $scope.slides;

  	$scope.myInterval = 5000;
  	$scope.noWrapSlides = false;
  	$scope.active = 0;
  	
  	var currIndex = 0;
  	
  	$scope.get_auction = function(auction){
  		window.location.assign(auction.url)

  	}

	$scope.openCarouselImg = function(picObj){
		reportService.getReport(picObj)
	}



	$scope.goToLogin = function(){
		$location.path('join');
	}



	for ( var image in $scope.imageri ){
		switch($scope.imageri [image]['title']) {

		    case 'IMAGEN1':
				$scope.image1 =$scope. imageri[image]['image'];
		        break;

		    case 'IMAGEN2':
				$scope.image2 = $scope.imageri[image]['image'];
		        break;

		    case 'IMAGEN3':
				$scope.image3 = $scope.imageri[image]['image'];
		        break;

		    case 'IMAGEN4':
				$scope.image4 = $scope.imageri[image]['image'];
		        break;		        

		    default:
		    	break;
		} 

	}
}])

hmShipControllers.controller('paymentMethodController', ['$scope', '$rootScope', '$window', 'shoppingCart', '$http', '$location', function( $scope, $rootScope, $window, shoppingCart, $http, $location ){
	
	$scope.shoppingCart = shoppingCart;
	$scope.pageClass = 'page-payment-method';
	$scope.myInterval = 5000;
	$scope.noWrapSlides = false;
	$scope.active = 0;

  	var currIndex = 0;
	function cartServiceIds(shoppingCart){
		var service_list = [];
		for (var i in shoppingCart){
			service_list.push(shoppingCart[i].id)
		}
		return service_list;
	}

	$scope.checkout = function(){

		if($scope.paymentMethodForm.$valid){
			
			if($scope.paymentMethod == 'deposit'){
				$location.path('checkout_deposit');
			}else{
				var data = {};
				var url = '/api/' + String($scope.paymentMethod) + '/';
				data.service_id_list = cartServiceIds($scope.shoppingCart);
				$http.post(url, data).success(function(redirect_url, status) {
					if(status == 200){
						window.location = redirect_url;
					}
				}).error(function(errors, status){
					console.log(errors);
				})		
			}

		}
	}
}])


hmShipControllers.controller('emailVerifiedController', ['$scope', '$rootScope', '$window',function( $scope, $rootScope, $window ){
	//$scope.token = sessionStorage.getItem('token');

}])

hmShipControllers.controller('editProductController', ['$scope', '$window', 'productsList', '$uibModal', '$http', 'yearListService',function( $scope, $window, productsList, $uibModal, $http, yearListService  ){
	
	$scope.yearRange = yearListService.request()
	// $scope.minDate = new Date()
	$scope.transclusion = {}
	$scope.transclusion.dateRange = 'last30';
	$scope.selectAll = false;
	// $scope.maxDate = new Date()
	//$scope.yearRange = ['2017', '2016']
	//$scope.DDSelection = 'last 30 days'
	//$scope.dateRange = 'last30';
	$scope.purchases = productsList;
	$scope.results_count = 0;
	$scope.typeAhead = ['Item in OrderBook'];


	$scope.refreshList = function(){
		$scope.purchases = productsList;
		$scope.results_count = 0;
		$scope.transclusion.dateRange = 'last30';
	}

	$scope.searchBackend = function(){
		var url = 'api/auctionproducts?search_param=' + $scope.searchParam
		$http.get(url).success(function(response ){
			
			if(response.length == 0){
				$scope.results = '0 Results Found;'
			}else{
				$scope.searchParam = '';
				$scope.purchases = response;
			}
		})	
	}

	$scope.queryDate = function(dateRange){

		switch(dateRange) {

		    case 'last30':
		    	var now_date = new Date()
		    	var timestamp_lte = new Date();
		        var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
		        break;

		    case 'months-6':
		    	var now_date = new Date()
		    	var timestamp_lte = new Date();
		        var timestamp_gte = new Date(  parseInt(now_date.setMonth(now_date.getMonth() - 6)))
		        break;

		    default:
		    	var timestamp_gte = new Date(  parseInt( dateRange ), 0, 1 );
		        var  timestamp_lte = new Date(  parseInt( dateRange ), 11, 31 );
		} 


		var url = 'api/auctionproducts?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
		
		$http.get(url).success(function(response ){
			
			if(response.length == 0){
				$scope.results = '0 Results Found;'
			}else{
				$scope.purchases = response;
				$scope.searchParam = '';
				
			}
		})	
	
	}



	$scope.itemInfo = function(row){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/purchasedetailsModal.html',
            controller: 'purchaseDetailsController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              item: function(){
                return row;
              }
            }
        });
	}

	$scope.auctionInfo = function(AuctionData){

        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/auctionDetailsModal.html',
            controller: 'auctionDetailsModalController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
                auctionDetails: function(){
                    return AuctionData;
              }
            }
        });
	}

	$scope.eraseSelection = function (){
		var del_list = [];
		for (var row in $scope.purchases){
			if ($scope.purchases[row].checked == true && $scope.purchases[row].services.services_present == false){
				del_list.push($scope.purchases[row].id)
			}
		}
		if (del_list.length == 0){
			alert('Please select the items you wish to delete');
			return false;
		}
		var delete_answer =  confirm("Are you sure you wish to delete the selected purchases?");
		var data = {}
		data.del_list  = del_list
		var url = 'api/deleteauctionproducts/';
		if (delete_answer){
			$http.post(url, data).success(function(purchases, status){
				
				if(status == 200){
					alert('Your auction purchases have been deleted');
					$scope.purchases = purchases;
				}
			})

		}else{
			return false;
		}
		
	}


	$scope.selectAllChx = function(){
		
		$scope.selectAll = !$scope.selectAll;
		for (var i in $scope.purchases){
			if($scope.purchases[i].services.services_present == false){
				$scope.purchases[i].checked = $scope.selectAll;
			}
	
		}
	}

	$scope.changePurchase = function(row){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/purchaseModal.html',
            controller: 'purchaseModifyController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
				purchaseInfo: function(){
				return row;
				},
				auctionList: function($http) {
				    var url = 'api/auctions?auction_open=True';
				    return $http({ 
				        method: 'GET', 
				        url: url
				    }).then(function(response){
				        return response.data;
				    })
				} 
            }
        });
	}

	$scope.colList = [ 
		{'key':'id', 'title':'Item'}, 
		{'key':'lot_number', 'title':'Lot Number'}, 
		{'key':'host', 'title':'Auction'}, 
		//{'key':'auction_begin', 'title':'Auction Date'}, 
		{'key':'edit', 'title':'Modify'}, 
		// {'key':'id', 'title':'Status'}
	];

	$scope.auctionProductTabList = [
		//{ url : 'auctionproducts', name : 'Register Purchases'  },
		{ url : 'editauctionproducts', name : 'Edit Purchases'  },
		{ url : 'orderbook', name : 'Order Book'  },
		//{ url : 'orderhistory', name : 'Order History'  },
		//{ url : 'paymenthistory', name : 'Payment History'  }
		{ url : 'paymenthistory', name : 'Payment History'  }
	]



}])




hmShipControllers.controller('maintenanceController', ['$scope', 'userProducts', '$http', '$location', '$rootScope', function( $scope, userProducts, $http, $location, $rootScope ){
	
	$scope.maintainanceProducts = userProducts;
	$scope.partsProvider  = 'Client';
	$scope.locationData = {};
	$scope.pageClass = 'maintenance';
	$scope.requestMaintainance = function(){
		var formData = {};
		formData.products = $scope.auctionItem;
		formData.maintenanceType = $scope.maintenanceType;
		formData.location = $scope.location;
		formData.description = $scope.details;
		formData.parts_provider = $scope.partsProvider;
		formData.maintenance_type = $scope.maintenanceType;
		$http.post( 'api/maintenance/' , formData).success(function(response, status){
				if (status === 200){
					$scope.auctionItem = '';
					$scope.maintenanceType = '';
					$scope.location = '';
					$scope.description = '';
					$scope.maintenanceForm.$setUntouched();
					$scope.maintenanceForm.$setPristine();
					$rootScope.requestedserviceType = 'Maintenance';
					$location.path('serviceRequestThanks');
				}
		});
	}

}])

hmShipControllers.controller('inspectionsController', ['$scope', 'userProducts', '$http', '$location', '$rootScope', 'inspectionTypes',  '$uibModal', function( $scope, userProducts, $http, $location, $rootScope, inspectionTypes, $uibModal){
	
	$scope.inspectionProducts = userProducts;
	$scope.inspectionTypes = inspectionTypes;

	$scope.pageClass = 'inspections';
	$scope.locationData = {};

	function getInspectionSections(  ){
		for ( var i in $scope.inspectionTypes ){
			if($scope.inspectionTypes[i].id == $scope.inspectionType){
				return $scope.inspectionTypes[i]
			}
			
		}
	}



	$scope.showInspectionInfo = function(){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/inspectionInfoModal.html',
            controller: 'inspectionInfoModalController',
            size: 'lg',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              inspection_type_info: function(){
                return getInspectionSections();
              }

            }
        });
	}

	$scope.requestInspection = function(){
		var formData = {};
		formData.products = $scope.auctionItem;
		formData.inspection_type = $scope.inspectionType;
		formData.location = $scope.location;
		formData.description = $scope.description;
		$http.post( 'api/inspection/' , formData).success(function(response, status){
				if (status === 200){

					$rootScope.requestedserviceType = 'Inspection';
					$location.path('serviceRequestThanks');
				}
		});
	}

}])




hmShipControllers.controller('uploadProductController', ['$scope',
'Upload',
'$http',
'auctionList',
'$uibModal',
function( $scope, Upload, $http, auctionList, $uibModal ){

	$scope.uploadFields = {};
	$scope.optionsList = auctionList;
	$scope.showSuccessMessage = true;

	// $scope.auctionProductTabList = [
	// 	{ url : 'auctionproducts', name : 'Register Purchases'  },
	// 	{ url : 'editauctionproducts', name : 'Edit Purchases'  },
	// 	{ url : 'paymenthistory', name : 'Payment History'  }
	// ]



	$scope.picPreview = function(size, file){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            animation: $scope.animationsEnabled,
            templateUrl: '/static/templates/userapp/partials/productPicturepreview.html',
            controller: 'productPicturePreviewController',
            size: 'md',
            resolve: {//MAKES INMUEBLES LOCAL SCOPE PASSED TO MODAL CONTROLLER IN LINE 186
              mobilePhoto: function(){
                return file;
              }
            }
        });
	}


	$scope.select = function(event, file) {
	    $scope.selectedFile = file;
	}



    $scope.uploadProduct = function(file) {
    	if ($scope.uploadProductForm.$valid){
			
			$scope.f = file;
		    file.upload = Upload.upload({
		      url: 'api/auctionproducts/',
		      data: {
		      	auction : $scope.uploadFields.auctionName,
		      	lot_number: $scope.uploadFields.lotnumber, 
		      	image1: file,
		      	description: $scope.uploadFields.description,
		      	item_name : $scope.uploadFields.item_name
		      },
		    });

		    file.upload.then(function (response) {
				$scope.uploadFields = {};
				$scope.uploadProductForm.$setUntouched();
				$scope.uploadProductForm.$setPristine();
				//$scope.showSuccessMessage = true;
				$scope.selectedFile = undefined;

				//alert('Product Succesfully Uploaded, you may now request services for your purchases!');

		        var modalInstance = $uibModal.open({
		            ariaLabelledBy: 'modal-title',
		            ariaDescribedBy: 'modal-body',
		            animation: $scope.animationsEnabled,
		            templateUrl: '/static/templates/userapp/partials/post_product_modal.html',
		            controller: 'post_product_modalController',
		            size: 'md'
		            // resolve: {
		            //   mobilePhoto: function(){
		            //     return file;
		            //   }
		            // }
		        });
				//$scope.f = undefined;

		    }, function (response) {
		      if (response.status > 0)
		        $scope.errorMsg = response.status + ': ' + response.data;
		    	$scope.showSuccessMessage = false;
		    }, function (evt) {
		      // Math.min is to fix IE which reports 200% sometimes
		      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
		    });
		    }
    }
}])

