import typing

import k5test
import pytest

import krb5


@pytest.mark.requires_api("set_password")
def test_set_password(realm: k5test.K5Realm) -> None:
    ctx = krb5.init_context()
    princ = krb5.parse_name_flags(ctx, f"userexp@{realm.realm}".encode())
    opt = krb5.get_init_creds_opt_alloc(ctx)

    with pytest.raises(krb5.Krb5Error) as exc:
        krb5.get_init_creds_password(ctx, princ, opt, password=realm.password("user").encode())
    assert exc.value.err_code == -1765328361

    creds = krb5.get_init_creds_password(ctx, princ, opt, realm.password("user").encode(), in_tkt_service=b"kadmin/changepw")
    assert isinstance(creds, krb5.Creds)

    newpw = realm.password("user").encode()
    result = krb5.set_password(ctx, creds, newpw, princ)

    creds = krb5.get_init_creds_password(ctx, princ, opt, newpw)
    assert isinstance(creds, krb5.Creds)
