{ buildPythonPackage, pygithub }:

buildPythonPackage {
  pname = "github-gitea-mirror";
  version = "1.4.0";
  src = ./.;

  propagatedBuildInputs = [ pygithub ];
}
