export class Util {
  public static isEmpty(object: Object): boolean {
    return Object.getOwnPropertyNames(object).length === 0;
  }

}
