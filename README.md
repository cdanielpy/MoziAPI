MoziAPI
=======

Utilería prototipo de administración de interacción Python - Base de Datos.-

##  Componentes
A continuación se describe cada clase del proyecto y sus funciones dentro del mismo.-

### [ConectorBase](https://github.com/cdanielpy/MoziAPI/wiki/ConectorBase)
_Clase base para utilerías de conexión a motores de bases de datos._

La finalidad de esta clase es estandarizar los métodos de ejecución de comandos contra los diferentes motores de base de datos, un nivel por encima de [DB-API](http://legacy.python.org/dev/peps/pep-0249/), valiéndose de los métodos implementados por los mismos módulos externos existentes para cada motor, como mysql, sql server, oracle, sqlite, etc.-

Esta clase no debe ser utilizada directamente, debe ser implementada por otras, pues la idea es, en un futuro cercano, integrarla con otras clases y establecer un mejor control de las sesiones de datos.-

### OTDBase
_Clase base para modelo de tablas de bases de datos._

Esta clase esta "inspirada" en los _Entities_ de EJB en Java y el patrón _Value Object_, la idea es que sea un lugar centralizado donde definir la estructura de la representación de clase de una tabla e instancias de datos contenidos en sus registros.-

### Restriccion
_Clase para generación de criterios de Restricción de resultados._

Esta clase permite abstraer la generación de filtros _"where"_ de una sentencia sql a partir de simples métodos que hacen refencia al tipo de restricción a establecer.-

### Unión
_Clase para generación de sentencias con intersección de tablas._

Esta clase permite generar los comandos de vinculación entre tablas, es decir, los segmentos _"join"_ y las relaciones entre las tablas, éstas deben establecerse por medio de instancias de la clase **_Restriccion_**.

En caso que se desee establecer una relación de _"producto cartesiano"_ o _"cross join"_, la restricción se debe proveer por una comparación de valores simple y de _"relleno"_.-

    Ej.
    
    emp = Employee(cAlias = '_emp_')
    emp.unir(Union(_dep_ = DepEmp
                   , cTipo = Union.NORMAL
                   , oRestriccion = Restriccion.Ig('1', '1')
                   )
             )

	Lo que generará la siguiente cláusula:
    
    SELECT _emp_.emp_no, ... FROM employees AS _emp_ JOIN dept_emp AS _dep_ ON 1 = 1

## Versión 0.0.1b

Para esta versión inicial, sólo se soportan las siguientes características:

- **OTDBase**

	Relación de atributos de clase - campos de tabla por medio de un diccionario escrito manualmente.-
    No se administran más datos que los nombres de cada campo, más adelante veré de incluir una clase que permita manejar atributos como tipo, si acepta NULL, etc.-
    
- **Restricción**

	Se incluyen la mayoría de los comandos más comunmente requeridos en una sentencia SQL.-
    
- **Union**
	
    Soporte para la generación de uniones entre tablas.-

	Sólo tipos _JOIN, LEFT OUTER JOIN y RIGHT OUTHER JOIN_, implementados y probados.
    
    Evaluando si es mejor un método por tipo o implementar un método único especificando el tipo por medio de constantes.-

- **Relación entre clases**
    
    Soporte para relación entre clases que representan tablas relacionadas. Esto se logra por medio de decoradores de métodos y propiedades (property). Además de un método de la clase _**ConexionBase**_.-


## Ejemplo de Uso

Se incluyen un par de _proyectos de ejemplos_, dónde se muestra el uso de cada clase por medio de una conexión a una base de datos MySQL.-
