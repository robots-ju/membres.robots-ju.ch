<!DOCTYPE HTML>
<html>
	<head>
		<title>Plateforme membres Robots-JU</title>
		<meta charset="UTF-8" />
		
		<link rel="stylesheet" type="text/css" href="css/login.css">
		<link rel="stylesheet" href="css/uikit-rtl.css">
        <link rel="stylesheet" href="css/uikit-rtl.min.css"/>
        <link rel="stylesheet" href="css/uikit.css"/>
        <link rel="stylesheet" href="css/uikit.min.css"/>
        
        <script src="js/uikit-icons.js"></script>
        <script src="js/uikit-icons.min.js"></script>
        <script src="js/uikit.js"></script>
        <script src="js/uikit.min.js"></script>
	</head>

	<body>		
		<div class="container">    
			<h1>Intranet Robots-JU</h1>
			<p>Bienvenue sur la platerforme membres Robots-JU !</p>
		</div>
		<div class="box">
			<fieldset class="boxBody">
				<label>Nom d'utilisateur:</label>
				<input type="text" id="username">
				<label>Mot de passe:</label>
				<input type="password">
			</fieldset>
			<footer>
				<button id="btnLogin"><a href="accueil.php">Login</a></button>
			</footer>
		</div>
		<script>
			document.getElementById("btnLogin").onclick=function(){
				let response = await fetch("/login?user="+document.getElementById("username").value+"&pwd="+document.getElementById("password"));

				if (response.status==204) {
					document.location="/user.html";
				} else {
					alert("Nom d'utilisateur ou mot de passe invalide");
				}
			}
		</script>
	</body>
</html>