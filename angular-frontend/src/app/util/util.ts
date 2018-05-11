export class Util {
  public static isEmpty(object: Object) {
    return Object.getOwnPropertyNames(object).length === 0;
  }

}
