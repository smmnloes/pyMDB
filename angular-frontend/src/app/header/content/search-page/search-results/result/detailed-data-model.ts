export class DetailedDataModel {

  constructor(public credits: string[][],
              public budget: number,
              public originalLanguage: string,
              public productionCountries: string[],
              public releaseDate: Date,
              public posterPath: string,
              public overview: string,
              public hasDetails: boolean) {
  }

  public static createEmptyDetails(): DetailedDataModel {
    return new DetailedDataModel(null, null, null, null, null,
      null, null, false)
  }
}
