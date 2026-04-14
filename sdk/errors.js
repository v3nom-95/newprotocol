export class QAIError extends Error {
  constructor(code, message, details = undefined) {
    super(message);
    this.name = "QAIError";
    this.code = code;
    this.details = details;
  }
}
