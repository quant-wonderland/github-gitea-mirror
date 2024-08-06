{ buildPythonPackage, pygithub }:

buildPythonPackage {
  pname = "github-gitea-mirror";
  version = "1.0.0";
  src = ./.;

  propagatedBuildInputs = [ pygithub ];
}
