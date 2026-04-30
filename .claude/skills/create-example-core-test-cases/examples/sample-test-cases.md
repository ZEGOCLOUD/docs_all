# Example: ZIM Simple Chat - Core Test Cases

## test-cases.md Example

Below is an example of core test cases for a ZIM chat demo. Notice how it focuses on **core happy-path flows** and skips edge cases like empty input validation, duplicate contacts, or message persistence.

```markdown
# Test Cases - ZIM Simple Chat (Web)

> Platform: Web | Users: 2 (Alice, Bob) | Core features only

## Test Cases

| TC# | Device/Tab | Test Case | Steps | Expected Result |
|-----|-----------|-----------|-------|-----------------|
| TC-01 | Tab: alice | Login - Alice | Enter User ID `user_alice`, User Name `Alice`, click Login button | Main page loads with Chats/Contacts/Me tabs visible |
| TC-02 | Tab: bob | Login - Bob | Enter User ID `user_bob`, User Name `Bob`, click Login button | Main page loads with Chats/Contacts/Me tabs visible |
| TC-03 | Tab: alice | Add Contact | Go to Contacts tab, enter User ID `user_bob`, Name `Bob`, click Add | Bob appears in the contact list |
| TC-04 | Tab: alice | Send Message | Click Bob's contact to open chat, type `Hello Bob!`, press Enter | Message `Hello Bob!` appears as a sent bubble (green, right side) |
| TC-05 | Tab: bob | Receive Message | Go to Chats tab | Conversation with `user_alice` shows with last message `Hello Bob!` |
| TC-06 | Tab: bob | Reply Message | Open conversation with Alice, type `Hi Alice!`, press Enter | Message `Hi Alice!` appears as a sent bubble |
| TC-07 | Tab: alice | Receive Reply | Check current chat | Message `Hi Alice!` appears as a received bubble (white, left side) |
```

## Key Design Decisions

1. **7 test cases** cover the core flow: login → add contact → send → receive → reply → receive. This is sufficient for an example project.

2. **Skipped intentionally** (non-core for an example):
   - Empty field validation
   - Duplicate contact prevention
   - Logout/re-login
   - Message history persistence
   - Empty message prevention
   - Navigation edge cases

3. **Multi-user flow**: TC-04 and TC-05 form a send-receive pair; TC-06 and TC-07 form another. This validates the core real-time messaging capability.

4. **Device/Tab column**: Clearly specifies which tab/device performs each action, essential for multi-user scenarios.
