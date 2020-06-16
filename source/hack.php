<body bgcolor="red">
	<center>
		<br><br><br>
		<?php
			$id = $_GET['id'];
			$pw = $_GET['pw'];
			ECHO "<font size=200>"."<b><당신의 계정 정보가 해킹당했습니다!>"."<br><br><br><br>";
			ECHO "<font size=200>"."당신의 ID : ".$id."<br><br><br><br>";
			ECHO "<font size=200>"."당신의 PW : ".$pw;
			ECHO "<script>alert('당신의 계정 정보가 해킹당했습니다!');</script>";
		?>
	</center>
</body>