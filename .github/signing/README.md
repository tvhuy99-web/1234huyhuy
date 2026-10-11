# Stable public debug signing (AudioDefence)

`stable-debug.keystore.b64` is an intentionally **PUBLIC test signing key**.
It is for the fixed Android package `com.audiodefence.android` when running
`assembleDebug`. It allows GitHub-hosted runners and local build machines to
produce update-compatible APKs without a new random debug key each time.

- Key format: PKCS12, base64-encoded text committed to the repository.
- Alias: `audiodefence-stable-debug`.
- Store/key password: `android` (public test password).
- SHA-256 certificate: `FE:16:06:AE:04:59:E6:82:3E:54:9A:4F:50:40:4B:59:E2:63:19:8D:DA:30:B3:3E:CC:1A:7F:3D:4B:E9:ED:5D`.

**Do not regenerate, replace, or delete this file** if APK updates should
continue working. Both the GitHub Actions workflow and Gradle always use it.

Anyone who can read this repository can sign an APK with this test key.
Therefore it authenticates no publisher, is **not suitable for a secure
production release**, and must never be reused to sign a release identity.
Use the independently configured `AD_KEYSTORE` for signed releases.

The first APK signed with this new key cannot update old random-key Debug APKs,
nor an original publisher's APK. Back up game progress and migrate once.
See [the Vietnamese update guide](../../docs/APK_UPDATE_SIGNING.md).
