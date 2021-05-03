<!DOCTYPE html>
<html>

<body>

  <h1>Vislice</h1>

  <h2>Do sedaj si pravilno uganil</h2>
  <h3>{{ igra.pravilni_del_gesla() }}</h3>
  <h2>Do sedaj si narobe uganil</h2>
  <h3>{{ igra.nepravilni_ugibi() }}</h3>

  % if stanje == "W":
  <h3>Zmagal si :)</h3>
  % elif stanje == "X":
  <h3>Izgubil si</h3>
    <h4>Prava beseda je bila:{{ igra.geslo }}</h4>
  % else:
  <form method="POST">
    <label>
      Vnesi črko:
      <input type="text" name="ugibana_crka">
    </label>
    <input type="submit">UGIBAJ!</input>
  </form>  
  % end




</body>

</html>