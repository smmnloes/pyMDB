export class DetailedDataModel {

  constructor(public credits:string[][],
              public budget:number,
              public originalLanguage:string,
              public productionCountries:string[],
              public releaseDate:Date,
              public posterPath:string,
              public original_title:string) {
  }
}
