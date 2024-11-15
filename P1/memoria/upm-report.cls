\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{upm-report}  %[2023-05-31 v1.0 UPM Report Template]

\LoadClass[12pt,a4paper,oneside]{book}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Nos aseguramos de que usamos xetex como motor de compilación
%
\RequirePackage{ifxetex}
\RequireXeTeX

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Paquetes globales
%
\RequirePackage[titletoc]{appendix}  % Que aparezca "Apéndice"
\RequirePackage{awesomebox}  % Bloques de texto más molones
\RequirePackage{changepage}  % Para poder usar los adjustwidth
\RequirePackage{csquotes}  % Facilitar el trabajo con citas
\RequirePackage{eso-pic}  % Colores y fondos
\RequirePackage{graphicx}  % Mejoras sobre el paquete graphics
\RequirePackage{hologo}  % Para poner logos relacionados con LaTeX
\RequirePackage{ifthen}  % Para poder usar condicionales en la clase
\RequirePackage{pdflscape}  % Posibilidad de páginas en apaisado
\RequirePackage{xcolor}  % Mejoras sobre el paquete color
%\RequirePackage{algorithm}
%\RequirePackage{algpseudocode}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Valores constantes
%
\def\universityname{Universidad Politécnica de Madrid}
\def\templaterepository{https://github.com/blazaid/UPM-Report-Template}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Opciones de la clase
%
\RequirePackage{kvoptions} % Para usar argumentos al importar la clase
\SetupKeyvalOptions{family=@upm, prefix=@upm@}

% Opciones de configuración de la clase
\DeclareStringOption{type}
\DeclareStringOption{school}
\DeclareStringOption{degree}
\ProcessKeyvalOptions*

% Variables relacionadas con el tipo de memoria (arg. `type`)
\newcommand{\reporttype}{}
\newcommand{\reporttypeabbr}{}
\renewcommand{\reporttype}{Práctica de Administración y Gestión de Redes}
\renewcommand{\reporttypeabbr}{PAGR}

% Variables relacionadas con la escuela (arg. `school`)
\newcommand{\schoolname}{NO DEFINIDO}
\newcommand{\schoolabbr}{NO DEFINIDO}
\newcommand{\schoollogo}{NO DEFINIDO}
\newcommand{\schoollogoblackbackground}{NO DEFINIDO}
\newcommand{\schooladdress}{NO DEFINIDO}
\newcommand{\degreecode}{NO DEFINIDO}
\newcommand{\degreename}{NO DEFINIDO}
\ifthenelse{\equal{\@upm@school}{etsiaab}}{%
    % Datos de la escuela
    \renewcommand{\schoolname}{E.T.S. de Ingeniería Agronómica, Alimentaria y de Biosistemas}
    \renewcommand{\schoolabbr}{ETSIAAB}
    \renewcommand{\schoollogo}{upm-report/images/etsiaab-logotipo.png}
    \renewcommand{\schoollogoblackbackground}{upm-report/images/etsiaab-logotipo.png}
    \renewcommand{\schooladdress}{%
        Campus Ciudad Universitaria\\
        Av. Puerta de Hierro, nº 2 - 4\\
        28040 Madrid, España
    }
    \definecolor{schoolcolor}{RGB}{99,178,76}
    \definecolor{linkcolor}{RGB}{99,178,76}
}{
\ifthenelse{\equal{\@upm@school}{etsidi}}{%
    % Datos de la escuela
    \renewcommand{\schoolname}{E.T.S. de Ingeniería y Diseño Industrial}
    \renewcommand{\schoolabbr}{ETSIDI}
    \renewcommand{\schoollogo}{upm-report/images/etsidi-logotipo.png}
    \renewcommand{\schoollogoblackbackground}{upm-report/images/etsidi-logotipo-fondonegro.pdf}
    \renewcommand{\schooladdress}{%
        c/ Ronda de Valencia, 3\\
        28012, Madrid, España
    }
    \definecolor{schoolcolor}{RGB}{223,30,64}
    \definecolor{linkcolor}{RGB}{223,30,64}
}{
%% ETSISI
\ifthenelse{\equal{\@upm@school}{etsisi}}{%
    % Datos de la escuela
    \renewcommand{\schoolname}{E.T.S. de Ingeniería de Sistemas Informáticos}
    \renewcommand{\schoolabbr}{ETSISI}
    \renewcommand{\schoollogo}{upm-report/images/etsisi-isotipo.pdf}
    \renewcommand{\schoollogoblackbackground}{upm-report/images/etsisi-isotipo-white.pdf}
    \renewcommand{\schooladdress}{%
        Campus Sur UPM, Carretera de Valencia (A-3), km. 7\\
        28031, Madrid, España
    }
    \definecolor{schoolcolor}{RGB}{0,114,206}
    \definecolor{linkcolor}{RGB}{0,114,206}
}{
\ifthenelse{\equal{\schoolname}{}}{
    \PackageError{upm-report}{School}{Falta el parámetro 'school'}
}{}}}}


% Variables relacionadas con la titulación (arg. `degree`)

%% ETSAAB
\ifthenelse{\equal{\@upm@degree}{20BT}}{
    \renewcommand{\degreecode}{20BT}
    \renewcommand{\degreename}{Grado en Biotecnología}
}{
\ifthenelse{\equal{\@upm@degree}{20BI}}{
    \renewcommand{\degreecode}{20BI}
    \renewcommand{\degreename}{Grado en Ciencias Agrarias y Bioeconomía}
}{
\ifthenelse{\equal{\@upm@degree}{20IG}}{
    \renewcommand{\degreecode}{20IG}
    \renewcommand{\degreename}{Grado en Ingeniería Agrícola}
}{
\ifthenelse{\equal{\@upm@degree}{02IA}}{
    \renewcommand{\degreecode}{20IA}
    \renewcommand{\degreename}{Grado en Ingeniería Agroambiental}
}{
\ifthenelse{\equal{\@upm@degree}{20IA}}{
    \renewcommand{\degreecode}{20IA}
    \renewcommand{\degreename}{Grado en Ingeniería Alimentaria}
}{
%% ETSIDI
\ifthenelse{\equal{\@upm@degree}{56IE}}{
    \renewcommand{\degreecode}{56IE}
    \renewcommand{\degreename}{Grado en Ingeniería Eléctrica}
}{
\ifthenelse{\equal{\@upm@degree}{56IA}}{
    \renewcommand{\degreecode}{56IA}
    \renewcommand{\degreename}{Grado en Ingeniería Electrónica Industrial y Automática}
}{
\ifthenelse{\equal{\@upm@degree}{56IM}}{
    \renewcommand{\degreecode}{56IM}
    \renewcommand{\degreename}{Grado en Ingeniería Mecánica}
}{
\ifthenelse{\equal{\@upm@degree}{56IQ}}{
    \renewcommand{\degreecode}{56IQ}
    \renewcommand{\degreename}{Grado en Ingeniería Química}
}{
\ifthenelse{\equal{\@upm@degree}{56DD}}{
    \renewcommand{\degreecode}{56DD}
    \renewcommand{\degreename}{Grado en Ingeniería en Diseño Industrial y Desarrollo de Producto}
}{
%% ETSISI
\ifthenelse{\equal{\@upm@degree}{61CD}}{
    \renewcommand{\degreecode}{61CD}
    \renewcommand{\degreename}{Grado en Ciencia de Datos e Inteligencia Artificial}
}{
\ifthenelse{\equal{\@upm@degree}{61CI}}{
    \renewcommand{\degreecode}{61CI}
    \renewcommand{\degreename}{Grado en Ingeniería de Computadores}
}{
\ifthenelse{\equal{\@upm@degree}{61IW}}{
    \renewcommand{\degreecode}{61IW}
    \renewcommand{\degreename}{Grado en Ingeniería del Software}
}{
\ifthenelse{\equal{\@upm@degree}{61SI}}{
    \renewcommand{\degreecode}{61SI}
    \renewcommand{\degreename}{Grado en Sistemas de Información}
}{
\ifthenelse{\equal{\@upm@degree}{61TI}}{
    \renewcommand{\degreecode}{61TI}
    \renewcommand{\degreename}{Grado en Tecnologías para la Sociedad de la Información}
}{
\ifthenelse{\equal{\@upm@degree}{MAADM}}{
    \renewcommand{\degreecode}{MAADM}
    \renewcommand{\degreename}{Máster Universitario en Aprendizaje Automático y Datos Masivos}
}{
\ifthenelse{\equal{\@upm@degree}{MPBD}}{
    \renewcommand{\degreecode}{MPBD}
    \renewcommand{\degreename}{Máster en Proyectos Big Data}
}{
\ifthenelse{\equal{\degreecode}{}}{
    \PackageError{upm-report}{Degree}{Falta el parámetro 'degree'}
}{}}}}}}}}}}}}}}}}}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Autores, directores y demás
%
\renewcommand{\and}{y\space}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Variables
%
\makeatletter
\newcommand{\bibauthor}[1]{\gdef\@bibauthor{#1}}%
\newcommand{\@bibauthor}{\@latex@warning@no@line{No \noexpand\bibauthor given}}
\newcommand{\director}[1]{\gdef\@director{#1}}%
\newcommand{\@director}{\@latex@warning@no@line{No \noexpand\director given}}
\newcommand{\bibdirector}[1]{\gdef\@bibdirector{#1}}%
\newcommand{\@bibdirector}{\@latex@warning@no@line{No \noexpand\bibdirector given}}

\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Idioma
%
\RequirePackage[spanish,es-tabla,es-ucroman]{babel}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Geometría general de las páginas
%
\RequirePackage[
    top=3.5cm,
    bottom=3cm,
    left=2.5cm,
    right=2.5cm,
]{geometry}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cabeceras y pies de página
%
\RequirePackage{fancyhdr}
\setlength{\headheight}{15.8pt}
\pagestyle{fancy}

% Estilos globales
\fancyhf{}
\fancyhead[L]{\textcolor{schoolcolor}{\sffamily\nouppercase{\rightmark}}}
\fancyhead[R]{\textcolor{schoolcolor}{\sffamily\thepage}}
\renewcommand{\headrulewidth}{0.5pt}

% Estilos en páginas "plain" (e.g. primera de capítulo)
\fancypagestyle{plain}{%
    \fancyhf{}
    \renewcommand{\headrule}{}
    \renewcommand{\footrule}{}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Estilos de capítulo, sección, ...
%
\RequirePackage{titlesec}

\titleformat{\chapter}%
    {\fontsize{30}{30}}%
    {\sffamily\fontsize{30}{30}\color{schoolcolor}\thechapter.}%
    {0.6em}%
    {\sffamily\fontsize{30}{30}\raggedleft\hspace*{\fill}}
    [\hrule]
\titlespacing*{\chapter}{0pt}{0pt}{25pt}

\titleformat{\section}%
    {}{\sffamily\huge\thesection.}{0.6em}{\sffamily\huge}
\titleformat{\subsection}%
    {}{\sffamily\Large\thesubsection.}{0.6em}{\sffamily\Large}
\titleformat{\subsubsection}%
    {}{\sffamily\large\thesubsubsection.}{0.6em}{\sffamily\large}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Estilos de la tabla de contenidos
%
\RequirePackage{titletoc}
\setcounter{tocdepth}{1}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Fuentes
%
\RequirePackage{fontspec}  % Para importar fuentes externas
\RequirePackage{microtype} % Mejoras tipográficas generales
% TODO Cambiar los tipos de letra según la guía de estilos de la escuela
\setmainfont[
    Path=upm-report/fonts/Montserrat/,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-SemiBold,
    ItalicFont=*-Italic,
    BoldItalicFont=*-SemiBoldItalic,
]{Montserrat}

\setsansfont[
    Path=upm-report/fonts/Barlow Condensed/,
    Extension=.ttf,
    UprightFont=*-Medium,
    BoldFont=*-Bold,
    ItalicFont=*-MediumItalic,
    BoldItalicFont=*-BoldItalic,
]{BarlowCondensed}

\setmonofont[
    Path=upm-report/fonts/Fira Code/,
    Extension=.ttf,
    UprightFont=*-regular,
    BoldFont=*-bold,
]{firacode}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Fórmulas matemáticas
%
\RequirePackage{amsmath}   % Mejoras presentación matemática
\RequirePackage{mathtools} % Más mejoras de presentación matemática

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Configuración de figuras y tablas
%
\RequirePackage{float}      % Mejorar colocación de elementos flotantes
\RequirePackage{tabularx}   % Tablas más configurables
\newcolumntype{C}{%
    >{\centering\arraybackslash}X%
    }                       % Para tener columnas tipo X centradas
\RequirePackage{booktabs}   % Configuraciones para tablas más bonitas
\RequirePackage{caption}    % Mejora de pies de figuras
\RequirePackage{subcaption} % Pies de subfiguras


\DeclareCaptionFormat{caption-upm}{#1#2~\small #3}
\DeclareCaptionLabelFormat{caption-upm}{\textbf{#1 #2}}
\DeclareCaptionLabelSeparator{caption-upm}{.}

\captionsetup{
    format=caption-upm,
    labelformat=caption-upm,
    labelsep=caption-upm,
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Configuración general de espaciados, geometrías y otros
%
\setlength{\parskip}{1em}
\linespread{1.2}
\setlength{\parindent}{0pt}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Configuración para PDF e hipervínculos
%
\RequirePackage[naturalnames]{hyperref}
\makeatletter
\hypersetup{
    pdfauthor={\@author},
    pdftitle={\@title},
    %pdfsubject={},   % TODO PONER ALGUNA OPCIÓN PARA DETERMINAR EL TEMA
    %pdfkeywords={},  % TODO QUE LAS KEYWORDS SE USEN TAMBIÉN AQUÍ
    pdfcreator={\@author},
    pdfproducer={},
    breaklinks=true,
    linktoc=all,
    plainpages=false,
    unicode=true,
    colorlinks=true,
    anchorcolor={linkcolor},
    citecolor={linkcolor},
    linkcolor={linkcolor},
    urlcolor={linkcolor},
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Estilos de los listados de código fuente
%
\RequirePackage{listings}
\renewcommand{\lstlistingname}{Listado}
\renewcommand*{\lstlistlistingname}{Índice de listados}

\makeatletter
\renewcommand\lstlistoflistings{\bgroup
  \let\contentsname\lstlistlistingname
  \def\l@lstlisting##1##2{\@dottedtocline{1}{1.5em}{2.3em}{##1}{##2}}
  \let\lst@temp\@starttoc \def\@starttoc##1{\lst@temp{lol}}%
  \tableofcontents \egroup}
\makeatother

\definecolor{sbase03}{HTML}{002B36}
\definecolor{sbase02}{HTML}{073642}
\definecolor{sbase01}{HTML}{586E75}
\definecolor{sbase00}{HTML}{657B83}
\definecolor{sbase0}{HTML}{839496}
\definecolor{sbase1}{HTML}{93A1A1}
\definecolor{sbase2}{HTML}{EEE8D5}
\definecolor{sbase3}{HTML}{FDF6E3}
\definecolor{syellow}{HTML}{B58900}
\definecolor{sorange}{HTML}{CB4B16}
\definecolor{sred}{HTML}{DC322F}
\definecolor{smagenta}{HTML}{D33682}
\definecolor{sviolet}{HTML}{6C71C4}
\definecolor{sblue}{HTML}{268BD2}
\definecolor{scyan}{HTML}{2AA198}
\definecolor{sgreen}{HTML}{859900}
\lstset{
    sensitive=true,
    aboveskip=\baselineskip,
    belowskip=\baselineskip,
    frame=lines,
    xleftmargin=\parindent,
    belowcaptionskip=1\baselineskip,
    basicstyle=\color{sbase00}\ttfamily,
    keywordstyle=\color{scyan},
    commentstyle=\color{sbase1},
    stringstyle=\color{sblue},
    numberstyle=\color{sviolet},
    identifierstyle=\color{sbase00},
    breaklines=true,
    showstringspaces=false,
    tabsize=2
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Listados condicionales
%
\RequirePackage[
    figure,table,lstlisting,equation
    ]{totalcount}  % Contar las veces que aparecen entradas en listados

\newcommand\conditionalLoF{\iftotalfigures\listoffigures\fi}
\newcommand\conditionalLoT{\iftotaltables\listoftables\fi}
\newcommand\conditionalLoL{\iftotallstlistings\lstlistoflistings\fi}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Referencias y bibliografía
%
\RequirePackage[backend=biber,style=ieee]{biblatex}
\RequirePackage{xurl}
\def\UrlBreaks{
    \do\/\do-\do\0\do\1\do\2\do\3\do\4\do\5\do\6\do\7\do\8\do\9
    \do\a\do\b\do\c\do\d\do\e\do\f\do\g\do\h\do\i\do\j\do\k\do\l\do\m
    \do\n\do\o\do\p\do\q\do\r\do\s\do\t\do\u\do\v\do\w\do\x\do\y\do\z
    \do\A\do\B\do\C\do\D\do\E\do\F\do\G\do\H\do\I\do\J\do\K\do\L\do\M
    \do\N\do\O\do\P\do\Q\do\R\do\S\do\T\do\U\do\V\do\W\do\X\do\Y\do\Z
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Portada
%
\makeatletter         
\renewcommand\maketitle{{
    \sffamily
    \thispagestyle{empty}
    % Barra lateral izquierda y logo fondo
    \AddToShipoutPicture*{%
        \AtPageLowerLeft{%
            \makebox[1\paperwidth][r]{%
                \includegraphics[width=0.9\paperwidth]{upm-report/images/upm-logotipo}
            }%
        }
        \put(0,0){%
            \colorbox{schoolcolor}{%
                \parbox[b][\paperheight]{2cm}{\vfill\hfill}
            }%
        }
    }
    \begin{adjustwidth}{0.5cm}{}
        {\normalsize \MakeUppercase{\universityname}}\\*[0.5em]
        {\normalsize \MakeUppercase{\textbf{\schoolname}}}\\*[0.5em]
        {\normalsize \MakeUppercase{\reporttype}}\\*[0.5em]
        {\normalsize \MakeUppercase{\textbf{\degreename}}}
        \vfill
        \begin{hyphenrules}{nohyphenation}
        \raggedright
        \begin{sloppypar}\fontsize{34}{34}\selectfont\bfseries\@title\end{sloppypar}
        \end{hyphenrules}
        \vfill
        \parbox[b]{\linewidth}{
            \normalsize
            \textbf{Desarrollado por}: \@author \\*[0.5em]
            Madrid, \@date
        }
    \end{adjustwidth}
    \normalfont
    \normalsize
}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Licencia
%
\makeatletter
\newcommand\makelicense{{
    \footnotesize
    \clearpage
    \thispagestyle{empty}
    ~\vfill
    \par{
        \textit{\@title}\\
        \textbf{Desarrollado por}: \@author\\
        \reporttype, \today\\
    }
    
    \par{
        \textbf{\schoolname}\\
        \schooladdress
    }
    \newline
    \hrule
    \vspace*{-0.5cm}\par{\licencia}
 }}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Agradecimientos
%
\makeatletter
\newcommand{\acknowledgements}[1]{\gdef\@acknowledgements{#1}}%
\newcommand{\@acknowledgements}{}
\newcommand\makeacknowledgements{{
    \ifthenelse{\equal{\@acknowledgements}{}}{}{
        \clearpage
        \thispagestyle{empty}
        \chapter*{Agradecimientos}
        \@acknowledgements
    }
}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cubierta trasera
%
\makeatletter         
\newcommand{\makebackcover}{
    \clearpage
    \thispagestyle{empty}
    \pagecolor{schoolcolor}
    \AddToShipoutPicture*{%
        \put(0,0){%
            \colorbox{black}{%
                \parbox[b][.5\paperheight]{\paperwidth}{\vfill\hfill}
            }%
        }
    }
    \vspace*{\fill}
    \begin{center}
        \includegraphics[width=.35\paperheight]{\schoollogoblackbackground}
    \end{center}
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Elementos del comienzo del documento
%
\makeatletter
\AtBeginDocument{%
    \maketitle
    \makelicense
    \makeacknowledgements
    \makeresumen
    \makeabstract
    
    \frontmatter

    \begingroup
        \tableofcontents
        \conditionalLoF
        \conditionalLoT
        \conditionalLoL
    \endgroup

    \mainmatter
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Elementos del fin del documento
%
\makeatletter
\AtEndDocument{
    \backmatter

    \renewcommand\bibname{Referencias}
    \printbibliography
    \makebackcover
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Añadimos el fichero con las entradas de las referencias bibliográficas
%
\addbibresource{references.bib}

\endinput