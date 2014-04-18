MoziAPI
=======

Utilería prototipo de administración de interacción Python - Base de Datos.-

##  Componentes
A continuación se describe cada clase del proyecto y sus funciones dentro del mismo.-

### ConectorBase
_Clase base para utilerias de conexión a motores de bases de datos._

La finalidad de esta clase es estandarizar los metodos de ejecución de comandos contra los diferentes motores de base de datos, un nivel por encima de [DB-API](http://legacy.python.org/dev/peps/pep-0249/), valiéndose de los métodos implementados por los mismos modulos externos existentes para cada motor, como mysql, sql server, oracle, sqlite, etc.-

Esta clase no debe ser utilizada directamente, debe ser implementada por otras pues la idea es, en un futuro cercano, integrarla con otras clases y establecer un mejor control de las sesiones de datos.-

### OTDBase
_Clase base para modelo de tablas de bases de datos._

Esta clase esta "inspirada" en los_ Entities_ de EJB de Java y el patrón _Value Object_, la idea es que sea un lugar centralizado donde definir la estructura de la representacion de clase de una tabla e instancias de datos contenidos en sus registros.-

### Restriccion
_Clase para generación de criterios de Restriccion de resultados._

Esta clase permite abstraer la generación de filtros _"where"_ de una sentencia sql a partir de simples métodos que hacen refencia al tipo de restricción a establecer.-

### Unión
_Clase para generación de sentencias con intersección de tablas._

Esta clase permite generar los comandos de vinculación entre tablas, es decir, los segmentos _"join"_, no así la relación entre los campos de enlace entre las mismas, éstas deben establecerse por medio de instancias de la clase **_Restriccion_**, salvo caso que se desee establecer una relación de _"producto cartesiano"_ o _"cross join"_.-

## Versión 0.0.1

Para esta versión inicial, sólo se soportan las siguientes características:

- **OTDBase**

	Relación de atributos de clase - campos de tabla por medio de un diccionario escrito manualmente.-
    No se administran más datos que los nombres de cada campo, más adelante veré de incluir una clase que permita manejar atributos como tipo, si acepta NULL, etc.-
    
- **Restriccion**

	Se incluyen la mayoría de los comandos más comunmente requeridos en una sentencia SQL.-
    
- **Union**
	
    Soporte sólo para la unión entre dos tablas, siguiente paso será la posibilidad de vincular más de ellas.-

	Sólo de tipo _JOIN_, implementado y probado.
    
    Evaluando si es mejor un método por tipo o implementar un método único especificando el tipo por medio de constantes.-

## Ejemplo de Uso

Se incluye un _proyecto de test_, dónde se muestra el uso de cada clase por medio de una conexión a una base de datos MySQL.-


