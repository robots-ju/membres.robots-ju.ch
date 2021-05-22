<!DOCTYPE HTML>
<html>
	<head>
		<link rel="shortcut icon" href="media/favicon.png"/>
		<title>Page d'accueil</title>
		<meta charset="UTF-8" />
		
		<link rel="stylesheet" href="css/login.css">
		<link rel="stylesheet" href="css/structure.css">
		<link rel="stylesheet" href="css/uikit-rtl.css">
        <link rel="stylesheet" href="css/uikit-rtl.min.css"/>
        <link rel="stylesheet" href="css/uikit.css"/>
        <link rel="stylesheet" href="css/uikit.min.css"/>
        
        <script src="js/uikit-icons.js"></script>
        <script src="js/uikit-icons.min.js"></script>
        <script src="js/uikit.js"></script>
        <script src="js/uikit.min.js"></script>
	</head>

	<header">
		<nav class="uk-navbar-container" uk-navbar>
			<div class="uk-navbar-left">
				<ul class="uk-navbar-nav">					
					<li class="uk-width-large" style="background-color: #478a23;"><a href="accueil.php" class="uk-align-right" style="color: #FFFFFF"><p class="uk-text-large">ROBOTS-JU</p></a></li>
					<li class="uk-width-small"><a href="#"><p style="color: #000000">Ateliers FLL</p></a></li>
					<li class="uk-width-small"><a href="#"><p style="color: #000000">Ateliers Avancés</p></a></li>
					<li class="uk-width-small"><a href="#"><p style="color: #000000">Photos</p></a></li>
					<li class="uk-width-small"><a href="membres.php"><p style="color: #000000">Membres</p></a></li>
				</ul>
			</div>
			<div class="uk-navbar">
				<ul class="uk-navbar-nav">
					<li><a href="#"><p style="color: #000000">Espace public</p></a></li>
				</ul>
			</div>
		</nav>
	</header>

	<body>		
		<div class="uk-position-relative uk-visible-toggle uk-light" uk-slideshow="autoplay: true" tabindex="-1" uk-slideshow>
			<ul class="uk-slideshow-items">
				<li>
					<img class="img" src="media/accueil/SuperSam.JPG" alt="" uk-cover>
				</li>

				<li>
					<img class="img" src="media/accueil/TeamJura1.JPG" alt="" uk-cover>
				</li>

				<li>
					<img class="img" src="media/accueil/TeamJura2.JPG" alt="" uk-cover>
				</li>

				<li>
					<img class="img" src="media/accueil/TeamJura3.JPG" alt="" uk-cover>
				</li>

				<li>
					<img class="img" src="media/accueil/TeamJura4.JPG" alt="" uk-cover>
				</li>
			</ul>
			<a class="uk-position-center-left uk-position-small uk-hidden-hover" href="#" uk-slidenav-previous uk-slideshow-item="previous"></a>
			<a class="uk-position-center-right uk-position-small uk-hidden-hover" href="#" uk-slidenav-next uk-slideshow-item="next"></a>
		</div>
	</body>
</html>