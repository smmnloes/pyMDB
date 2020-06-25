import {Iso639} from "../../../../../util/iso639";

export class DetailedDataModel {

  constructor(public credits: string[][],
              public budget: number,
              public originalLanguage: string,
              public productionCountries: string[],
              public releaseDate: string,
              public posterPath: string,
              public overview: string,
              public hasDetails: boolean) {
  }

  public hasPosterPath(): boolean {
    return this.posterPath != null;
  }

  public static createEmptyDetails(): DetailedDataModel {
    return new DetailedDataModel(null, null, null, null, null,
      null, null, false)
  }

  static fromJSON(json: Object) {
    return new DetailedDataModel(
      DetailedDataModel.processCredits(json['credits']),
      json['budget'],
      Iso639.iso639ToName[json['original_language']],
      json['production_countries'].map(element => element['name']),
      formatReleaseDate(json['release_date']),
      json['poster_path'],
      json['overview'],
      true);
  }

  private static processCredits(credits: Object): string[][] {
    let creditsProcessed: string[][] = [];

    for (let cast of credits['cast']) {
      creditsProcessed.push([cast['name'], cast['character']]);
    }
    return creditsProcessed;
  }
}

function formatReleaseDate(jsonElement: any): string {
  let date: Date = new Date(jsonElement);
  if (isInvalidDate(date)) {
    return null;
  }
  let options = {month: '2-digit', day: '2-digit', year: 'numeric'};
  return date.toLocaleDateString('en', options)
}


function isInvalidDate(date: Date) {
  return isNaN(date.getDay());
}

