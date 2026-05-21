%global debug_package %{nil}

Name:           python3-flag-attention
Version:        0.3.0
Release:        1%{?dist}
Summary:        FlagAttention — memory-efficient attention operators (Triton)

License:        Apache-2.0
URL:            https://github.com/flagos-ai/FlagAttention
Source0:        flag-attention-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 60
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-setuptools_scm

%description
Collection of memory-efficient attention operators implemented in the Triton language, for large language model training and inference.

%prep
%autosetup -n flag-attention-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=0.3.0
%pyproject_wheel

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=0.3.0
%pyproject_install
%pyproject_save_files flag_attn

%check
# Smoke find_spec test (no actual import) — verifies the built module
# lands at the expected sitelib path. Doesn't import the module so
# missing runtime deps (torch, triton, ...) don't trip the check;
# those are user-install-time concerns, not packaging concerns.
PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python3 -c "import importlib.util; s = importlib.util.find_spec('flag_attn'); assert s and s.origin, 'flag_attn not findable'; print('OK: flag_attn at', s.origin)"

%files -f %{pyproject_files}
%license LICENSE*

%changelog
* Wed May 13 2026 FlagOS Contributors <contact@flagos.io> - 0.3.0-1
- Initial RPM packaging.
